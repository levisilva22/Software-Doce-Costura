from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import ServiceClient
from django.conf import settings
import requests
import logging

logger = logging.getLogger(__name__)

class AuthProxyView(APIView):
    """View para encaminhar requisições ao serviço de autenticação."""
    
    permission_classes = []  # Permitir acesso não autenticado para login/registro
    
    def post(self, request, *args, **kwargs):
        path = request.path.replace('/api/auth', '')
        
        # Log para debug
        logger.info(f"Encaminhando requisição para AUTH: {path}")
        

        try:
            # Encaminha a requisição ao serviço de autenticação
            data, status_code = ServiceClient.forward_request(
                service_name='AUTH',
                path=path,
                method='POST',
                data=request.data,
                headers=self._get_headers(request)
            )
            
            # Muito importante: Manter o código de status original para que o cliente
            # receba os erros de validação corretamente
            return Response(data=data, status=status_code)
            
        except Exception as e:
            logger.error(f"Erro ao encaminhar requisição para AUTH: {str(e)}")
            return Response(
                {"error": "Erro de comunicação com o serviço de autenticação"},
                status=500
            )
        
    def _get_headers(self, request):
        """Extrair cabeçalhos relevantes da requisição original."""
        headers = {}
        if 'Authorization' in request.headers:
            headers['Authorization'] = request.headers['Authorization']
        return headers


class RecommendationView(APIView):
    """View para encaminhar requisições ao serviço de recomendação."""
   
    
    def get(self, request, *args, **kwargs):
        path = request.path.replace('/api/recommendations', '')
        
        data, status_code = ServiceClient.forward_request(
            service_name='RECOMMENDATION',
            path=path,
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
    
    permission_classes = []  # Permitir acesso não autenticado
    
    def get(self, request, *args, **kwargs):
        path = request.path.replace('/api/products', '')
         
        
        # Passar os parâmetros de consulta
        data, status_code = ServiceClient.forward_request(
            service_name='MAIN',
            path=path,  # Usar o caminho correto para o serviço principal
            method='GET',
            headers=self._get_headers(request),
            params=request.query_params
        )
        
        return Response(data=data, status=status_code)
    
    def post(self, request, *args, **kwargs):
        path = request.path.replace('/api/products', '')
        
        data, status_code = ServiceClient.forward_request(
            service_name='MAIN',
            path=path,
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
            path=path,
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
            path=path,
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
