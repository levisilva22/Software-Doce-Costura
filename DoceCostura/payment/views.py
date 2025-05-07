from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Order, Payment, OrderItem
from .serializers import OrderSerializer, PaymentSerializer, CheckoutSerializer
from .services import PaymentService
from product.permissions import MicroservicePermission

class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar pedidos
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [MicroservicePermission]
    
    def get_queryset(self):
        """
        Filtra pedidos pelo usuário atual
        """
        user_id = self.request.user_data.get('id')
        if user_id:
            return Order.objects.filter(user_id=user_id)
        return Order.objects.none()
    
    @action(detail=False, methods=['post'])
    def checkout(self, request):
        """
        Processa checkout: converte carrinho em pedido e inicia pagamento
        """
        # Validar dados do checkout
        serializer = CheckoutSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user_id = request.user_data.get('id')
        if not user_id:
            return Response(
                {"error": "Usuário não autenticado"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Obter carrinho do usuário
        from product.models import Cart
        try:
            cart = Cart.objects.get(user_id=user_id, is_active=True)
            if not cart.items.exists():
                return Response(
                    {"error": "Carrinho está vazio"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Cart.DoesNotExist:
            return Response(
                {"error": "Carrinho não encontrado"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Criar pedido a partir do carrinho
        checkout_data = serializer.validated_data
        
        # 1. Criar o pedido
        order = Order.objects.create(
            user_id=user_id,
            shipping_address=checkout_data['address'],
            shipping_city=checkout_data['city'],
            shipping_state=checkout_data['state'],
            shipping_zipcode=checkout_data['zipcode'],
            subtotal=cart.subtotal,
            shipping_fee=checkout_data.get('shipping_fee', 0),
            discount=checkout_data.get('discount', 0),
            payment_method=checkout_data['payment_method'],
            total=cart.subtotal + checkout_data.get('shipping_fee', 0) - checkout_data.get('discount', 0)
        )
        
        # 2. Criar itens do pedido a partir dos itens do carrinho
        from product.models import Product
        for cart_item in cart.items.all():
            product = cart_item.product
            OrderItem.objects.create(
                order=order,
                product_id=product.id,
                product_name=product.name,
                quantity=cart_item.quantity,
                price=product.price
            )
            
            # Atualizar estoque
            product.stock -= cart_item.quantity
            product.save()
        
        # 3. Limpar o carrinho
        cart.is_active = False
        cart.save()
        
        # 4. Processar pagamento
        payment_result = PaymentService.process_payment(order, {
            'payment_method': checkout_data['payment_method'],
            **checkout_data.get('payment_details', {})
        })
        
        # 5. Retornar resultado
        order_serializer = OrderSerializer(order)
        return Response({
            'order': order_serializer.data,
            'payment': payment_result
        })
    
    @action(detail=True, methods=['get'])
    def payments(self, request, pk=None):
        """
        Lista pagamentos de um pedido
        """
        order = self.get_object()
        payments = order.payments.all()
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)
        
class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para consultar pagamentos
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [MicroservicePermission]
    
    def get_queryset(self):
        user_id = self.request.user_data.get('id')
        if user_id:
            return Payment.objects.filter(order__user_id=user_id)
        return Payment.objects.none()
    
    @action(detail=True, methods=['post'])
    def check_status(self, request, pk=None):
        """
        Verifica status atual do pagamento
        """
        payment = self.get_object()
        result = PaymentService.check_payment_status(payment.id)
        
        if result['success']:
            serializer = self.get_serializer(result['payment'])
            return Response(serializer.data)
        else:
            return Response(
                {"error": result['message']},
                status=status.HTTP_400_BAD_REQUEST
            )
