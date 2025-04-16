from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para criação e visualização de usuários
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'password_confirm', 
                 'first_name', 'last_name', 'phone_number']
        extra_kwargs = {
            'id': {'read_only': True},
            'email': {'required': True},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }
    
    def validate(self, attrs):
        # Validação para confirmar que as senhas coincidem
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({"password": "As senhas não correspondem."})
        
        # Remove o campo password_confirm após validação
        attrs.pop('password_confirm', None)
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer para visualização e atualização do perfil de usuário
    """
    profile_data = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 
                 'phone_number', 'created_at', 'updated_at', 'profile_data']
        read_only_fields = ['id', 'email', 'created_at', 'updated_at']
    
    def get_profile_data(self, obj):
        """
        Retorna dados do perfil relacionado, se existir
        """
        try:
            profile = obj.profile
            return {
                'bio': profile.bio,
                'date_of_birth': profile.date_of_birth,
                'address': profile.address,
                'country': profile.country,
                'city': profile.city,
                'postal_code': profile.postal_code,
                'profile_picture': profile.profile_picture,
            }
        except UserProfile.DoesNotExist:
            return {}


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer para alteração de senha
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs.get('new_password') != attrs.get('new_password_confirm'):
            raise serializers.ValidationError({"new_password": "As novas senhas não correspondem."})
        return attrs


class TokenValidationSerializer(serializers.Serializer):
    """
    Serializer para validação de tokens
    """
    token = serializers.CharField(required=True)


class TokenRefreshSerializer(serializers.Serializer):
    """
    Serializer para refresh de tokens
    """
    refresh = serializers.CharField(required=True)