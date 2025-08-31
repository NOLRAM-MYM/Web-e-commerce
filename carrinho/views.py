from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from produtos.models import Product
from .models import Cart, CartItem
import json


@login_required
def cart_view(request):
    """Visualizar carrinho de compras"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('product').all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': cart.total_price,
        'total_items': cart.total_items,
    }
    return render(request, 'carrinho/cart.html', context)


@login_required
@require_POST
def add_to_cart(request, product_id):
    """Adicionar produto ao carrinho"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity <= 0:
        messages.error(request, 'Quantidade deve ser maior que zero.')
        return redirect('core:product_detail', slug=product.slug)
    
    if quantity > product.stock_quantity:
        messages.error(request, f'Estoque insuficiente. Disponível: {product.stock_quantity}')
        return redirect('core:product_detail', slug=product.slug)
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    try:
        with transaction.atomic():
            cart_item, item_created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not item_created:
                new_quantity = cart_item.quantity + quantity
                if new_quantity > product.stock_quantity:
                    messages.error(request, f'Estoque insuficiente. Disponível: {product.stock_quantity}')
                    return redirect('core:product_detail', slug=product.slug)
                cart_item.quantity = new_quantity
                cart_item.save()
            
            messages.success(request, f'{product.name} adicionado ao carrinho!')
            
    except Exception as e:
        messages.error(request, 'Erro ao adicionar produto ao carrinho.')
    
    return redirect('core:product_detail', slug=product.slug)


@login_required
@require_POST
def remove_from_cart(request, item_id):
    """Remover item do carrinho"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    
    messages.success(request, f'{product_name} removido do carrinho.')
    return redirect('carrinho:cart')


@login_required
@require_POST
def update_cart_item(request, item_id):
    """Atualizar quantidade de item no carrinho"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity <= 0:
        cart_item.delete()
        messages.success(request, f'{cart_item.product.name} removido do carrinho.')
    elif quantity > cart_item.product.stock_quantity:
        messages.error(request, f'Estoque insuficiente. Disponível: {cart_item.product.stock_quantity}')
    else:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, 'Carrinho atualizado!')
    
    return redirect('carrinho:cart')


@login_required
@require_POST
def clear_cart(request):
    """Limpar carrinho"""
    try:
        cart = Cart.objects.get(user=request.user)
        cart.clear()
        messages.success(request, 'Carrinho limpo!')
    except Cart.DoesNotExist:
        pass
    
    return redirect('carrinho:cart')


@login_required
def cart_count(request):
    """API: Retornar número de itens no carrinho"""
    try:
        cart = Cart.objects.get(user=request.user)
        count = cart.total_items
    except Cart.DoesNotExist:
        count = 0
    
    return JsonResponse({'count': count})


@login_required
def cart_total(request):
    """API: Retornar total do carrinho"""
    try:
        cart = Cart.objects.get(user=request.user)
        total = float(cart.total_price)
    except Cart.DoesNotExist:
        total = 0.0
    
    return JsonResponse({'total': total})