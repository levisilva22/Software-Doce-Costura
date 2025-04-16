# api_gateway/gateway/middleware.py
import time
import logging
import uuid
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class RequestLoggerMiddleware(MiddlewareMixin):
    """Middleware para fazer log de todas as solicitações à API Gateway."""
    
    def process_request(self, request):
        # Gerar um ID de rastreamento para a solicitação
        request.trace_id = request.headers.get('X-Trace-ID', str(uuid.uuid4()))
        request.start_time = time.time()
        
        # Adicionar informações de log
        logger.info(
            f"Request started: {request.method} {request.path}",
            extra={
                'trace_id': request.trace_id,
                'method': request.method,
                'path': request.path,
                'user_id': request.user.id if request.user.is_authenticated else None
            }
        )
        return None
        
    def process_response(self, request, response):
        # Calcular duração da solicitação
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            logger.info(
                f"Request finished: {request.method} {request.path} - {response.status_code} in {duration:.2f}s",
                extra={
                    'trace_id': getattr(request, 'trace_id', None),
                    'status_code': response.status_code,
                    'duration': duration
                }
            )
            
        # Adicionar o ID de rastreamento à resposta
        if hasattr(request, 'trace_id'):
            response['X-Trace-ID'] = request.trace_id
            
        return response