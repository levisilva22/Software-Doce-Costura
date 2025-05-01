import jwt
import requests
from django.conf import settings

class JWTUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extrair e processar o token antes de passar para a view
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        # Adiciona um objeto user_data vazio por padrão
        request.user_data = {'id': None}
        
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                # Verificar via microserviço
                response = requests.post(
                    settings.AUTH_VALIDATE_TOKEN_ENDPOINT,
                    json={'token': token},
                    timeout=3
                )
                
                if response.status_code == 200:
                    request.user_data = response.json().get('user', {'id': None})
            except Exception:
                # Falha silenciosa - o user_data já tem um valor padrão
                pass
                
        return self.get_response(request)