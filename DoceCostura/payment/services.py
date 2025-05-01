# services.py
import uuid
from django.conf import settings
from .models import Order, Payment
import stripe
import mercadopago
from django.utils import timezone
import datetime
import requests
import json

class PaymentService:
    """
    Serviço para processar pagamentos com diferentes gateways
    """
    
    @staticmethod
    def process_payment(order, payment_data):
        """
        Processa um pagamento baseado no método escolhido
        """
        payment_method = payment_data.get('payment_method')
        
        # Cria um registro de pagamento
        payment = Payment.objects.create(
            order=order,
            amount=order.total,
            payment_method=payment_method,
            status='pending'
        )
        
        # Selecionar gateway de pagamento baseado no método
        if payment_method == 'credit_card':
            return PaymentService._process_credit_card(payment, payment_data)
        elif payment_method == 'pix':
            return PaymentService._process_pix(payment, payment_data)
        elif payment_method == 'boleto':
            return PaymentService._process_boleto(payment, payment_data)
        else:
            payment.status = 'declined'
            payment.transaction_data = {'error': 'Método de pagamento não suportado'}
            payment.save()
            return {
                'success': False,
                'message': 'Método de pagamento não suportado',
                'payment': payment
            }
    
    @staticmethod
    def _process_credit_card(payment, payment_data):
        """
        Processa pagamento com cartão de crédito via Stripe
        """
        try:
            
            # Configurar API key do Stripe
            stripe.api_key = settings.STRIPE_SECRET_KEY
            
            # Criar o pagamento no Stripe
            stripe_charge = stripe.Charge.create(
                amount=int(payment.amount * 100),  # Stripe usa centavos
                currency="brl",
                source=payment_data.get('token'),  # Token do cartão obtido no frontend
                description=f"Pedido #{payment.order.order_number}",
                metadata={
                    'order_id': str(payment.order.id),
                    'customer_id': str(payment.order.user_id)
                }
            )
            
            # Processar resposta do Stripe
            transaction_id = stripe_charge.id
            success = stripe_charge.status == 'succeeded'
            
            # Atualiza o pagamento
            payment.transaction_id = transaction_id
            payment.status = 'approved' if success else 'pending'
            payment.transaction_data = {
                'stripe_id': stripe_charge.id,
                'last4': stripe_charge.payment_method_details.card.last4,
                'brand': stripe_charge.payment_method_details.card.brand,
                'response_code': stripe_charge.outcome.type,
                'response': stripe_charge.outcome.seller_message,
            }
            payment.save()
            
            # Atualiza o pedido se pagamento aprovado
            if success:
                payment.order.mark_as_paid(payment.transaction_id)
            
            return {
                'success': success,
                'message': 'Pagamento aprovado' if success else 'Pagamento está sendo processado',
                'payment': payment
            }
            
        except stripe.error.CardError as e:
            # Erro do cartão (recusado, etc)
            payment.status = 'declined'
            payment.transaction_data = {
                'error': str(e),
                'error_code': e.code,
                'decline_code': e.decline_code,
            }
            payment.save()
            return {
                'success': False,
                'message': f'Erro no cartão: {e.user_message}',
                'payment': payment
            }
            
        except (stripe.error.StripeError, Exception) as e:
            # Outros erros
            payment.status = 'declined'
            payment.transaction_data = {'error': str(e)}
            payment.save()
            return {
                'success': False,
                'message': f'Erro ao processar pagamento: {str(e)}',
                'payment': payment
            }
    
    @staticmethod
    def _process_pix(payment, payment_data):
        """
        Gera um código PIX usando a API do MercadoPago
        """
        try:
                        
            # Configurar SDK do MercadoPago
            sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
            
            # Data de expiração (24 horas)
            expiration_date = timezone.now() + datetime.timedelta(hours=24)
            
            # Criar pagamento PIX
            payment_data = {
                "transaction_amount": float(payment.amount),
                "description": f"Pedido #{payment.order.order_number}",
                "payment_method_id": "pix",
                "payer": {
                    "email": payment_data.get('email', 'cliente@exemplo.com'),
                    "identification": {
                        "type": payment_data.get('document_type', 'CPF'),
                        "number": payment_data.get('document_number', '12345678909')
                    }
                },
                "date_of_expiration": expiration_date.strftime("%Y-%m-%dT%H:%M:%S.000-03:00")
            }
            
            payment_response = sdk.payment().create(payment_data)
            
            if payment_response["status"] == 201:
                mp_payment = payment_response["response"]
                
                # Extrair dados do PIX
                pix_data = mp_payment.get('point_of_interaction', {}).get('transaction_data', {})
                pix_code = pix_data.get('qr_code')
                qr_code_base64 = pix_data.get('qr_code_base64')
                
                # Atualizar registro de pagamento
                payment.transaction_id = str(mp_payment['id'])
                payment.status = 'pending'  # PIX sempre começa como pending
                payment.transaction_data = {
                    'pix_code': pix_code,
                    'qr_code_base64': qr_code_base64,
                    'expires_at': expiration_date.isoformat(),
                    'mercadopago_id': mp_payment['id'],
                    'payment_status': mp_payment['status']
                }
                payment.save()
                
                return {
                    'success': True,
                    'message': 'Código PIX gerado com sucesso',
                    'pix_data': payment.transaction_data,
                    'payment': payment
                }
            else:
                # Falha na criação do pagamento
                payment.status = 'declined'
                payment.transaction_data = {
                    'error': 'Falha ao gerar PIX',
                    'response': payment_response
                }
                payment.save()
                
                return {
                    'success': False,
                    'message': 'Não foi possível gerar o código PIX',
                    'payment': payment
                }
        
        except Exception as e:
            payment.status = 'declined'
            payment.transaction_data = {'error': str(e)}
            payment.save()
            
            return {
                'success': False,
                'message': f'Erro ao gerar PIX: {str(e)}',
                'payment': payment
            }
    
    @staticmethod
    def _process_boleto(payment, payment_data):
        """
        Gera um boleto usando a API da PagHiper
        """
        try:           
            # Configurações da PagHiper
            api_key = settings.PAGHIPER_API_KEY
            token = settings.PAGHIPER_TOKEN
            
            # Data de vencimento (3 dias úteis)
            due_date = (timezone.now() + datetime.timedelta(days=3)).strftime('%Y-%m-%d')
            
            # Preparar dados para a API
            payload = {
                "apiKey": api_key,
                "order_id": str(payment.order.order_number),
                "payer_email": payment_data.get('email', 'cliente@exemplo.com'),
                "payer_name": payment_data.get('name', 'Cliente Teste'),
                "payer_cpf_cnpj": payment_data.get('document', '12345678909'),
                "days_due_date": 3,
                "type_bank_slip": "boletoA4",
                "items": [
                    {
                        "description": f"Pedido #{payment.order.order_number}",
                        "quantity": 1,
                        "price_cents": int(payment.amount * 100)
                    }
                ]
            }
            
            # Chamar a API da PagHiper
            headers = {"Content-Type": "application/json"}
            response = requests.post(
                'https://api.paghiper.com/transaction/create/',
                data=json.dumps(payload),
                headers=headers
            )
            
            response_json = response.json()
            
            if response_json['result'] == 'success':
                transaction_data = response_json['transaction']
                
                # Atualizar registro de pagamento
                payment.transaction_id = transaction_data['transaction_id']
                payment.status = 'pending'
                payment.transaction_data = {
                    'barcode': transaction_data['bank_slip']['digitable_line'],
                    'pdf_url': transaction_data['bank_slip']['url_slip_pdf'],
                    'expiration_date': due_date,
                    'transaction_id': transaction_data['transaction_id'],
                    'url_slip': transaction_data['bank_slip']['url_slip']
                }
                payment.save()
                
                return {
                    'success': True,
                    'message': 'Boleto gerado com sucesso',
                    'boleto_data': payment.transaction_data,
                    'payment': payment
                }
            else:
                # Falha na criação do boleto
                payment.status = 'declined'
                payment.transaction_data = {
                    'error': 'Falha ao gerar boleto',
                    'response': response_json
                }
                payment.save()
                
                return {
                    'success': False,
                    'message': 'Não foi possível gerar o boleto',
                    'payment': payment
                }
        
        except Exception as e:
            payment.status = 'declined'
            payment.transaction_data = {'error': str(e)}
            payment.save()
            
            return {
                'success': False,
                'message': f'Erro ao gerar boleto: {str(e)}',
                'payment': payment
            }
    
    @staticmethod
    def check_payment_status(payment_id):
        """
        Verifica o status de um pagamento pendente no gateway
        """
        try:
            payment = Payment.objects.get(id=payment_id)
            
            if payment.status != 'pending':
                return {
                    'success': True,
                    'status': payment.status,
                    'payment': payment
                }
            
            # Verificar o status com base no método de pagamento
            if payment.payment_method == 'credit_card' and payment.transaction_id:
                return PaymentService._check_credit_card_status(payment)
            elif payment.payment_method == 'pix' and payment.transaction_id:
                return PaymentService._check_pix_status(payment)
            elif payment.payment_method == 'boleto' and payment.transaction_id:
                return PaymentService._check_boleto_status(payment)
            
            return {
                'success': True,
                'status': payment.status,
                'payment': payment,
                'message': 'Status não alterado'
            }
                
        except Payment.DoesNotExist:
            return {
                'success': False,
                'message': 'Pagamento não encontrado'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro ao verificar pagamento: {str(e)}'
            }

    @staticmethod
    def _check_credit_card_status(payment):
        """Verifica status de pagamento com cartão no Stripe"""
        import stripe
        from django.conf import settings
        
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        try:
            charge = stripe.Charge.retrieve(payment.transaction_id)
            
            # Mapear status do Stripe para nosso sistema
            status_map = {
                'succeeded': 'approved',
                'pending': 'pending',
                'failed': 'declined'
            }
            
            new_status = status_map.get(charge.status, 'pending')
            
            # Atualiza se o status mudou
            if new_status != payment.status:
                payment.status = new_status
                payment.save()
                
                if new_status == 'approved':
                    payment.order.mark_as_paid(payment.transaction_id)
            
            return {
                'success': True,
                'status': payment.status,
                'payment': payment
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro ao consultar status no Stripe: {str(e)}'
            }

    @staticmethod
    def _check_pix_status(payment):
        """Verifica status de pagamento PIX no MercadoPago"""
        import mercadopago
        from django.conf import settings
        
        sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
        
        try:
            mp_payment_id = payment.transaction_id
            response = sdk.payment().get(mp_payment_id)
            
            if response["status"] == 200:
                mp_payment = response["response"]
                
                # Mapear status do MercadoPago para nosso sistema
                status_map = {
                    'approved': 'approved',
                    'pending': 'pending',
                    'rejected': 'declined',
                    'cancelled': 'declined'
                }
                
                new_status = status_map.get(mp_payment['status'], 'pending')
                
                # Atualiza se o status mudou
                if new_status != payment.status:
                    payment.status = new_status
                    payment.save()
                    
                    if new_status == 'approved':
                        payment.order.mark_as_paid(payment.transaction_id)
                
                # Atualiza dados da transação
                payment.transaction_data.update({
                    'payment_status': mp_payment['status'],
                    'payment_status_detail': mp_payment['status_detail'],
                    'last_updated': mp_payment['date_last_updated']
                })
                payment.save()
                
            return {
                'success': True,
                'status': payment.status,
                'payment': payment
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro ao consultar status no MercadoPago: {str(e)}'
            }

    @staticmethod
    def _check_boleto_status(payment):
        """Verifica status de pagamento com boleto na PagHiper"""
        import requests
        import json
        from django.conf import settings
        
        try:
            # Configurações da PagHiper
            api_key = settings.PAGHIPER_API_KEY
            token = settings.PAGHIPER_TOKEN
            
            # Preparar dados para a API
            payload = {
                "apiKey": api_key,
                "token": token,
                "transaction_id": payment.transaction_id
            }
            
            # Chamar a API da PagHiper
            headers = {"Content-Type": "application/json"}
            response = requests.post(
                'https://api.paghiper.com/transaction/status/',
                data=json.dumps(payload),
                headers=headers
            )
            
            response_json = response.json()
            
            if response_json['result'] == 'success':
                status_data = response_json['status']
                
                # Mapear status da PagHiper para nosso sistema
                status_map = {
                    'paid': 'approved',
                    'pending': 'pending', 
                    'canceled': 'declined',
                    'refunded': 'refunded'
                }
                
                new_status = status_map.get(status_data['status'], 'pending')
                
                # Atualiza se o status mudou
                if new_status != payment.status:
                    payment.status = new_status
                    payment.save()
                    
                    if new_status == 'approved':
                        payment.order.mark_as_paid(payment.transaction_id)
                
                # Atualiza dados da transação
                payment.transaction_data.update({
                    'payment_status': status_data['status'],
                    'payment_date': status_data.get('paid_date', None)
                })
                payment.save()
                
            return {
                'success': True,
                'status': payment.status,
                'payment': payment
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro ao consultar status na PagHiper: {str(e)}'
            }