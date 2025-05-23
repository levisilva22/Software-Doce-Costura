import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class ServiceClient:
    """Cliente para comunicação com microserviços."""
    
    @staticmethod
    def forward_request(service_name, path, method='GET', data=None, headers=None, params=None):
        """
        Encaminha uma solicitação para um microserviço específico.
        
        Args:
            service_name: Nome do serviço (AUTH, RECOMMENDATION, etc.)
            path: Caminho da API no microserviço
            method: Método HTTP (GET, POST, etc.)
            data: Dados para enviar no corpo da requisição
            headers: Cabeçalhos HTTP
            params: Parâmetros de consulta
            
        Returns:
            Resposta do microserviço
        """
        if headers is None:
            headers = {}
            
        service_url = settings.MICROSERVICE_URLS.get(service_name)
        if not service_url:
            logger.error(f"Serviço não configurado: {service_name}")
            return {"error": "Service not configured"}, 500
            
        url = f"{service_url}{path}"
        logger.info(f"Enviando requisição para: {url}")
        
        print(f"DEBUG: ENviando requisição para {url}")
        print(f"DEBUG: urls do serviço {service_url}")

        try:
            response = requests.request(
                method=method,
                url=url,
                json=data if method in ['POST', 'PUT', 'PATCH'] else None,
                headers=headers,
                params=params
            )
            
            # Tentar obter a resposta JSON
            try:
                return response.json(), response.status_code
            except ValueError:
                # Se não for JSON, verificar se é um erro
                if response.status_code >= 400:
                    return {
                        "error": "Resposta inválida do serviço",
                        "message": response.text
                    }, response.status_code
                else:
                    return {"message": response.text}, response.status_code
            
        except requests.RequestException as e:
            logger.error(f"Erro ao comunicar com o serviço {service_name}: {str(e)}")
            return {"error": f"Service communication error: {str(e)}"}, 500