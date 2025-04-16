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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Criptografando a senha antes de salvar
        password = serializer.validated_data.pop('password', None)
        if password:
            serializer.validated_data['password'] = make_password(password)
            
        self.perform_create(serializer)
        
        # Gerando tokens para o novo usuário
        user = serializer.instance
        refresh = RefreshToken.for_user(user)
        
        response_data = {
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    """
    View para login de usuários, estendendo TokenObtainPairView
    para personalizar o comportamento
    """
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == status.HTTP_200_OK:
            # Adicionando informações extras na resposta
            user = User.objects.get(email=request.data['email'])
            response.data['user_id'] = str(user.id)
            response.data['email'] = user.email
            
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
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({"message": "Logout realizado com sucesso"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Token de refresh não fornecido"}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError as e:
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
