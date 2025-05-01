import requests
from rest_framework import permissions

class MicroservicePermission(permissions.BasePermission):
    """
    Permissão personalizada que verifica autorização via microserviço externo.
    """
    
    def has_permission(self, request, view):
        # Para requisições seguras (GET, HEAD, OPTIONS), permitir acesso
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Obter token de autenticação do cabeçalho
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return False
            
        token = auth_header.split(' ')[1]
        
        # Fazer requisição ao microserviço de autorização
        try:
            response = requests.post(
                'http://auth-microservice-url/api/auth/verify',
                json={
                    'token': token,
                    'resource': 'product',  # ou categoria, dependendo do viewset
                    'action': self._get_action_name(request.method, view)
                },
                timeout=3  # timeout em segundos
            )
            
            if response.status_code == 200:
                return response.json().get('authorized', False)
            return False
        except Exception:
            # Em caso de erro de conexão, negar acesso por segurança
            # Em produção, considere uma política de fallback
            return False
            
    def _get_action_name(self, method, view):
        """Converte o método HTTP para nome da ação correspondente"""
        if hasattr(view, 'action'):
            return view.action
        
        # Mapeamento padrão
        method_map = {
            'GET': 'list' if view.suffix == 'List' else 'retrieve',
            'POST': 'create',
            'PUT': 'update',
            'PATCH': 'partial_update',
            'DELETE': 'destroy'
        }
        return method_map.get(method, 'unknown')