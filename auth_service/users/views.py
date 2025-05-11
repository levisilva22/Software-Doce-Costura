from django.shortcuts import render
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .serializers import UserSerializer, UserProfileSerializer, PasswordChangeSerializer, TokenValidationSerializer, TokenRefreshSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """
    View para registro de novos usuários
    """
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data) # Serializer recebe os dados JSON vindos do request
        serializer.is_valid(raise_exception=True) # Valida os dados
        
        # Criptografando a senha antes de salvar
        password = serializer.validated_data.pop('password', None) # Apaga a senha do dicionário mas antes de remove-la ele retorna seu valor
        if password:
            serializer.validated_data['password'] = make_password(password) # Cripgrafa a senha
            
        self.perform_create(serializer) # Salva o usuário no banco de dados

        # Gerando tokens para o novo usuário
        user = serializer.instance # Obtém a referência ao objeto de usuário já criado no banco de dados
        refresh = RefreshToken.for_user(user) # Cria um token para o usuário
        
        # Cria o a resposta JSON vai ser enviado ao cliente
        response_data = {
            'user': serializer.data,
            'email': serializer.validated_data['email'],
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    """
    View para login de usuários, estendendo TokenObtainPairView
    para personalizar o comportamento
    """
    
    """
        Atualiza os dados da requisição para incluir o IP do usuário
        e adiciona informações extras na resposta.
        - Adiciona o ID do usuário e o email na resposta.
        - Registra o IP do usuário no campo last_login_ip.
        - O IP é obtido do cabeçalho HTTP_X_FORWARDED_FOR ou do REMOTE_ADDR.
        - O IP é salvo no banco de dados.   
    """
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == status.HTTP_200_OK:
            # Adicionando informações extras na resposta
            user = User.objects.get(email=request.data['email']) # Obtendo o usuário pelo email
            response.data['user_id'] = str(user.id)
            response.data['email'] = user.email
            response.data['username'] = user.username
            response.data['first_name'] = user.first_name
            
            # Registrando login
            if 'HTTP_X_FORWARDED_FOR' in request.META:
                ip = request.META['HTTP_X_FORWARDED_FOR'].split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR', '')
            
            user.last_login_ip = ip
            user.save(update_fields=['last_login_ip'])
            
        return response


class LogoutView(APIView):
    """
    View para logout de usuários
    """
    permission_classes = (permissions.IsAuthenticated,)  # Apenas usuários autenticados podem fazer logout
    
    def post(self, request):
        try:
            # Tenta obter o token de refresh enviado no corpo da requisição
            refresh_token = request.data.get('refresh')
            if refresh_token:
                # Converte a string do token em um objeto RefreshToken
                # Isso valida o formato e assinatura do token
                token = RefreshToken(refresh_token)
                
                # Adiciona o token à blacklist para invalidá-lo imediatamente
                # Mesmo que ainda não tenha expirado, não poderá mais ser usado
                token.blacklist()
                
                # Retorna uma mensagem de sucesso ao cliente
                return Response({"message": "Logout realizado com sucesso"}, status=status.HTTP_200_OK)
            else:
                # Se o token não foi fornecido na requisição, retorna erro
                return Response({"error": "Token de refresh não fornecido"}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError as e:
            # Captura erros relacionados ao token (formato inválido, expirado, etc.)
            # e retorna uma mensagem de erro com o detalhe do problema
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    View para visualizar e atualizar o perfil do usuário
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserProfileSerializer
    
    def get_object(self):
        return self.request.user


class TokenValidationView(APIView):
    """
    View para validar tokens JWT e fornecer informações do usuário
    para outros microserviços
    """
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request):
        token = request.data.get('token')
        
        if not token:
            return Response(
                {'error': 'Token não fornecido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Valida o token
            valid_token = AccessToken(token)
            
            # Extrai o ID do usuário
            user_id = valid_token.get('user_id')
            
            try:
                user = User.objects.get(id=user_id)
                return Response({
                    'valid': True,
                    'user_id': str(user.id),
                    'email': user.email,
                    'is_active': user.is_active,
                    'is_staff': user.is_staff,
                })
            except User.DoesNotExist:
                return Response(
                    {'error': 'Usuário não encontrado'},
                    status=status.HTTP_404_NOT_FOUND
                )
                
        except (InvalidToken, TokenError):
            return Response(
                {'valid': False, 'error': 'Token inválido ou expirado'},
                status=status.HTTP_401_UNAUTHORIZED
            )


class ChangePasswordView(APIView):
    """
    View para alteração de senha
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PasswordChangeSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {'error': 'Senha atual incorreta'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        # Invalidando tokens existentes
        RefreshToken.for_user(user)
        
        return Response(
            {'message': 'Senha alterada com sucesso'},
            status=status.HTTP_200_OK
        )


class RefreshTokenView(APIView):
    """
    View customizada para refresh de tokens
    """
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request):
        refresh_token = request.data.get('refresh')
        
        if not refresh_token:
            return Response(
                {'error': 'Token de refresh não fornecido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            
            return Response({
                'access': access_token,
                'refresh': str(refresh),
            })
        except TokenError:
            return Response(
                {'error': 'Token de refresh inválido ou expirado'},
                status=status.HTTP_401_UNAUTHORIZED
            )
