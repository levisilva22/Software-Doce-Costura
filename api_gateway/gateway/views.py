from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import ServiceClient

class AuthProxyView(APIView):
    """View para encaminhar requisições ao serviço de autenticação."""
    
    permission_classes = []  # Permitir acesso não autenticado para login/registro
    
    def post(self, request, *args, **kwargs):
        # Extrair o endpoint específico do path
        path = request.path.replace('/api/auth', '')
        
        data, status_code = ServiceClient.forward_request(
            service_name='AUTH',
            path=f"/api{path}",
            method='POST',
            data=request.data,
            headers=self._get_headers(request)
        )
        
        return Response(data=data, status=status_code)
        
    def _get_headers(self, request):
        """Extrair cabeçalhos relevantes da requisição original."""
        headers = {}
        if 'Authorization' in request.headers:
            headers['Authorization'] = request.headers['Authorization']
        return headers


class RecommendationView(APIView):
    """View para encaminhar requisições ao serviço de recomendação."""
    
    def get(self, request, *args, **kwargs):
        # Extrair o endpoint específico do path
        path = request.path.replace('/api/recommendations', '')
        
        data, status_code = ServiceClient.forward_request(
            service_name='RECOMMENDATION',
            path=f"/api{path}",
            method='GET',
            headers=self._get_headers(request),
            params=request.query_params
        )
        
        return Response(data=data, status=status_code)
        
    def _get_headers(self, request):
        """Extrair cabeçalhos relevantes da requisição original."""
        headers = {}
        if 'Authorization' in request.headers:
            headers['Authorization'] = request.headers['Authorization']
        return headers


class ProductsView(APIView):
    """View para encaminhar requisições ao serviço principal (produtos)."""
    
    def get(self, request, *args, **kwargs):
        path = request.path.replace('/api/products', '')
        
        data, status_code = ServiceClient.forward_request(
            service_name='MAIN',
            path=f"/api{path}",
            method='GET',
            headers=self._get_headers(request),
            params=request.query_params
        )
        
        return Response(data=data, status=status_code)
    
    def post(self, request, *args, **kwargs):
        path = request.path.replace('/api/products', '')
        
        data, status_code = ServiceClient.forward_request(
            service_name='MAIN',
            path=f"/api{path}",
            method='POST',
            data=request.data,
            headers=self._get_headers(request)
        )
        
        return Response(data=data, status=status_code)
    
    def _get_headers(self, request):
        headers = {}
        if 'Authorization' in request.headers:
            headers['Authorization'] = request.headers['Authorization']
        return headers


class PaymentProxyView(APIView):
    """View para encaminhar requisições ao serviço de pagamento."""
    
    def post(self, request, *args, **kwargs):
        # Extrair o endpoint específico do path
        path = request.path.replace('/api/payments', '')
        
        data, status_code = ServiceClient.forward_request(
            service_name='PAYMENT',
            path=f"/api{path}",
            method='POST',
            data=request.data,
            headers=self._get_headers(request)
        )
        
        return Response(data=data, status=status_code)
    
    def get(self, request, *args, **kwargs):
        # Lógica similar para GET requests
        path = request.path.replace('/api/payments', '')
        
        data, status_code = ServiceClient.forward_request(
            service_name='PAYMENT',
            path=f"/api{path}",
            method='GET',
            headers=self._get_headers(request)
        )
        
        return Response(data=data, status=status_code)
        
    def _get_headers(self, request):
        """Extrair cabeçalhos relevantes da requisição original."""
        headers = {}
        if 'Authorization' in request.headers:
            headers['Authorization'] = request.headers['Authorization']
        return headers
