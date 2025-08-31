from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.conf import settings
from django.core.paginator import Paginator
from carrinho.models import Cart
from .models import Order, OrderItem
import json
import paypalrestsdk
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

# Configurar PayPal
paypalrestsdk.configure({
    "mode": getattr(settings, 'PAYPAL_MODE', 'sandbox'),
    "client_id": getattr(settings, 'PAYPAL_CLIENT_ID', ''),
    "client_secret": getattr(settings, 'PAYPAL_CLIENT_SECRET', '')
})


@login_required
def order_list_view(request):
    """Listar pedidos do usuário"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    # Paginação
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'orders': page_obj,
    }
    return render(request, 'pedidos/order_list.html', context)


@login_required
def order_detail_view(request, order_number):
    """Detalhes do pedido"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    order_items = order.items.select_related('product').all()
    
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'pedidos/order_detail.html', context)


@login_required
def checkout_view(request):
    """Página de checkout"""
    try:
        cart = Cart.objects.get(user=request.user)
        if not cart.items.exists():
            messages.error(request, 'Seu carrinho está vazio.')
            return redirect('carrinho:cart')
    except Cart.DoesNotExist:
        messages.error(request, 'Seu carrinho está vazio.')
        return redirect('carrinho:cart')
    
    cart_items = cart.items.select_related('product').all()
    
    # Verificar estoque
    for item in cart_items:
        if item.quantity > item.product.stock_quantity:
            messages.error(request, f'Estoque insuficiente para {item.product.name}. Disponível: {item.product.stock_quantity}')
            return redirect('carrinho:cart')
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': cart.total_price,
        'paypal_client_id': settings.PAYPAL_CLIENT_ID,
    }
    return render(request, 'pedidos/checkout.html', context)


@login_required
def checkout_success_view(request):
    """Página de sucesso do checkout"""
    order_number = request.GET.get('order')
    if order_number:
        try:
            order = Order.objects.get(order_number=order_number, user=request.user)
            context = {'order': order}
            return render(request, 'pedidos/checkout_success.html', context)
        except Order.DoesNotExist:
            pass
    
    return render(request, 'pedidos/checkout_success.html')


def checkout_cancel_view(request):
    """Página de cancelamento do checkout"""
    messages.warning(request, 'Pagamento cancelado.')
    return render(request, 'pedidos/checkout_cancel.html')


@login_required
@require_POST
def create_paypal_payment(request):
    """Criar pagamento PayPal"""
    try:
        cart = Cart.objects.get(user=request.user)
        if not cart.items.exists():
            return JsonResponse({'error': 'Carrinho vazio'}, status=400)
        
        # Criar pedido
        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                total_amount=cart.total_price,
                currency='USD',  # Pode ser configurável
                status='pending',
                payment_method='paypal'
            )
            
            # Criar itens do pedido
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
        
        # Criar pagamento PayPal
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": request.build_absolute_uri(f"/pedidos/checkout/success/?order={order.order_number}"),
                "cancel_url": request.build_absolute_uri("/pedidos/checkout/cancel/")
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": item.product.name,
                        "sku": str(item.product.id),
                        "price": str(item.product.price),
                        "currency": "USD",
                        "quantity": item.quantity
                    } for item in cart.items.all()]
                },
                "amount": {
                    "total": str(cart.total_price),
                    "currency": "USD"
                },
                "description": f"Pedido #{order.order_number}"
            }]
        })
        
        if payment.create():
            # Salvar ID do pagamento
            order.payment_id = payment.id
            order.save()
            
            # Encontrar URL de aprovação
            for link in payment.links:
                if link.rel == "approval_url":
                    return JsonResponse({
                        'payment_id': payment.id,
                        'approval_url': link.href
                    })
        else:
            logger.error(f"PayPal payment creation failed: {payment.error}")
            order.delete()  # Remover pedido se pagamento falhou
            return JsonResponse({'error': 'Erro ao criar pagamento'}, status=500)
            
    except Exception as e:
        logger.error(f"Error creating PayPal payment: {str(e)}")
        return JsonResponse({'error': 'Erro interno'}, status=500)


@login_required
@require_POST
def execute_paypal_payment(request):
    """Executar pagamento PayPal"""
    try:
        data = json.loads(request.body)
        payment_id = data.get('payment_id')
        payer_id = data.get('payer_id')
        
        payment = paypalrestsdk.Payment.find(payment_id)
        
        if payment.execute({"payer_id": payer_id}):
            # Atualizar pedido
            try:
                order = Order.objects.get(payment_id=payment_id, user=request.user)
                order.status = 'paid'
                order.payment_status = 'completed'
                order.save()
                
                # Reduzir estoque
                for item in order.items.all():
                    product = item.product
                    product.stock_quantity -= item.quantity
                    product.save()
                
                # Limpar carrinho
                cart = Cart.objects.get(user=request.user)
                cart.clear()
                
                return JsonResponse({
                    'success': True,
                    'order_number': order.order_number
                })
                
            except Order.DoesNotExist:
                return JsonResponse({'error': 'Pedido não encontrado'}, status=404)
        else:
            logger.error(f"PayPal payment execution failed: {payment.error}")
            return JsonResponse({'error': 'Erro ao processar pagamento'}, status=500)
            
    except Exception as e:
        logger.error(f"Error executing PayPal payment: {str(e)}")
        return JsonResponse({'error': 'Erro interno'}, status=500)


@csrf_exempt
def paypal_webhook(request):
    """Webhook do PayPal para notificações"""
    if request.method == 'POST':
        try:
            # Processar webhook do PayPal
            # Implementar validação de webhook conforme documentação PayPal
            pass
        except Exception as e:
            logger.error(f"PayPal webhook error: {str(e)}")
    
    return HttpResponse(status=200)


@login_required
@require_POST
def cancel_order(request, order_number):
    """Cancelar pedido"""
    try:
        order = get_object_or_404(Order, order_number=order_number, user=request.user)
        
        if order.can_be_cancelled():
            order.status = 'cancelled'
            order.save()
            
            # Restaurar estoque se necessário
            if order.payment_status == 'completed':
                for item in order.items.all():
                    product = item.product
                    product.stock_quantity += item.quantity
                    product.save()
            
            return JsonResponse({'success': True, 'message': 'Pedido cancelado com sucesso'})
        else:
            return JsonResponse({'error': 'Pedido não pode ser cancelado'}, status=400)
            
    except Exception as e:
        logger.error(f"Error cancelling order: {str(e)}")
        return JsonResponse({'error': 'Erro interno'}, status=500)