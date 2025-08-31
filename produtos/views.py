from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db import transaction
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import Product, Category, ProductImage
from .forms import ProductForm, CategoryForm, ProductImageForm
import json
from PIL import Image
import os


def is_staff_user(user):
    """Verificar se usuário é staff"""
    return user.is_staff


@login_required
@user_passes_test(is_staff_user)
def product_admin_list(request):
    """Listar produtos para administração"""
    products = Product.objects.select_related('category').order_by('-created_at')
    
    # Filtros
    category_id = request.GET.get('category')
    search = request.GET.get('search')
    status = request.GET.get('status')
    
    if category_id:
        products = products.filter(category_id=category_id)
    
    if search:
        products = products.filter(
            name__icontains=search
        )
    
    if status == 'active':
        products = products.filter(is_active=True)
    elif status == 'inactive':
        products = products.filter(is_active=False)
    
    # Paginação
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        'page_obj': page_obj,
        'products': page_obj,
        'categories': categories,
        'current_category': category_id,
        'current_search': search,
        'current_status': status,
    }
    return render(request, 'produtos/admin/product_list.html', context)


@login_required
@user_passes_test(is_staff_user)
def product_admin_create(request):
    """Criar novo produto"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Produto "{product.name}" criado com sucesso!')
            return redirect('produtos:admin_list')
    else:
        form = ProductForm()
    
    context = {
        'form': form,
        'title': 'Criar Produto',
        'action': 'create'
    }
    return render(request, 'produtos/admin/product_form.html', context)


@login_required
@user_passes_test(is_staff_user)
def product_admin_edit(request, product_id):
    """Editar produto"""
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Produto "{product.name}" atualizado com sucesso!')
            return redirect('produtos:admin_list')
    else:
        form = ProductForm(instance=product)
    
    # Imagens do produto
    product_images = product.images.all()
    
    context = {
        'form': form,
        'product': product,
        'product_images': product_images,
        'title': f'Editar Produto: {product.name}',
        'action': 'edit'
    }
    return render(request, 'produtos/admin/product_form.html', context)


@login_required
@user_passes_test(is_staff_user)
@require_POST
def product_admin_delete(request, product_id):
    """Deletar produto"""
    product = get_object_or_404(Product, id=product_id)
    product_name = product.name
    
    try:
        product.delete()
        messages.success(request, f'Produto "{product_name}" deletado com sucesso!')
    except Exception as e:
        messages.error(request, f'Erro ao deletar produto: {str(e)}')
    
    return redirect('produtos:admin_list')


@login_required
@user_passes_test(is_staff_user)
def category_admin_list(request):
    """Listar categorias para administração"""
    categories = Category.objects.order_by('name')
    
    # Filtros
    search = request.GET.get('search')
    status = request.GET.get('status')
    
    if search:
        categories = categories.filter(name__icontains=search)
    
    if status == 'active':
        categories = categories.filter(is_active=True)
    elif status == 'inactive':
        categories = categories.filter(is_active=False)
    
    # Paginação
    paginator = Paginator(categories, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': page_obj,
        'current_search': search,
        'current_status': status,
    }
    return render(request, 'produtos/admin/category_list.html', context)


@login_required
@user_passes_test(is_staff_user)
def category_admin_create(request):
    """Criar nova categoria"""
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Categoria "{category.name}" criada com sucesso!')
            return redirect('produtos:category_admin_list')
    else:
        form = CategoryForm()
    
    context = {
        'form': form,
        'title': 'Criar Categoria',
        'action': 'create'
    }
    return render(request, 'produtos/admin/category_form.html', context)


@login_required
@user_passes_test(is_staff_user)
def category_admin_edit(request, category_id):
    """Editar categoria"""
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Categoria "{category.name}" atualizada com sucesso!')
            return redirect('produtos:category_admin_list')
    else:
        form = CategoryForm(instance=category)
    
    context = {
        'form': form,
        'category': category,
        'title': f'Editar Categoria: {category.name}',
        'action': 'edit'
    }
    return render(request, 'produtos/admin/category_form.html', context)


@login_required
@user_passes_test(is_staff_user)
@require_POST
def category_admin_delete(request, category_id):
    """Deletar categoria"""
    category = get_object_or_404(Category, id=category_id)
    category_name = category.name
    
    # Verificar se há produtos nesta categoria
    if category.products.exists():
        messages.error(request, f'Não é possível deletar a categoria "{category_name}" pois há produtos associados.')
        return redirect('produtos:category_admin_list')
    
    try:
        category.delete()
        messages.success(request, f'Categoria "{category_name}" deletada com sucesso!')
    except Exception as e:
        messages.error(request, f'Erro ao deletar categoria: {str(e)}')
    
    return redirect('produtos:category_admin_list')


def check_stock(request, product_id):
    """API: Verificar estoque do produto"""
    try:
        product = Product.objects.get(id=product_id, is_active=True)
        return JsonResponse({
            'available': product.stock_quantity,
            'in_stock': product.stock_quantity > 0
        })
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Produto não encontrado'}, status=404)


@login_required
@user_passes_test(is_staff_user)
@require_POST
def upload_product_image(request):
    """API: Upload de imagem do produto"""
    try:
        product_id = request.POST.get('product_id')
        image_file = request.FILES.get('image')
        
        if not product_id or not image_file:
            return JsonResponse({'error': 'Dados incompletos'}, status=400)
        
        product = get_object_or_404(Product, id=product_id)
        
        # Validar tipo de arquivo
        allowed_types = ['image/jpeg', 'image/png', 'image/webp']
        if image_file.content_type not in allowed_types:
            return JsonResponse({'error': 'Tipo de arquivo não permitido'}, status=400)
        
        # Validar tamanho (5MB max)
        if image_file.size > 5 * 1024 * 1024:
            return JsonResponse({'error': 'Arquivo muito grande (máximo 5MB)'}, status=400)
        
        # Criar imagem do produto
        product_image = ProductImage.objects.create(
            product=product,
            image=image_file,
            alt_text=f'Imagem de {product.name}'
        )
        
        return JsonResponse({
            'success': True,
            'image_id': product_image.id,
            'image_url': product_image.image.url,
            'alt_text': product_image.alt_text
        })
        
    except Exception as e:
        return JsonResponse({'error': f'Erro ao fazer upload: {str(e)}'}, status=500)