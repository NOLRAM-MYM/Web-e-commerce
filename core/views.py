from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from produtos.models import Product, Category
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


def home_view(request):
    """View da página inicial"""
    # Produtos em destaque (últimos 8 produtos ativos)
    featured_products = Product.objects.filter(is_active=True).order_by('-created_at')[:8]
    
    # Categorias principais
    categories = Category.objects.all()[:6]
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
        'page_title': 'Página Inicial'
    }
    
    return render(request, 'core/home.html', context)


def product_list_view(request):
    """View para listagem de produtos"""
    products = Product.objects.filter(is_active=True)
    
    # Filtros
    category_slug = request.GET.get('category')
    search_query = request.GET.get('q')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort_by = request.GET.get('sort', 'name')
    
    # Aplicar filtros
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass
    
    # Ordenação
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    elif sort_by == 'oldest':
        products = products.order_by('created_at')
    else:
        products = products.order_by('name')
    
    # Paginação
    paginator = Paginator(products, 12)  # 12 produtos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Categorias para filtro
    categories = Category.objects.all()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'current_category': category_slug,
        'search_query': search_query,
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by,
        'page_title': 'Produtos'
    }
    
    return render(request, 'core/product_list.html', context)


def product_detail_view(request, slug):
    """View para detalhes do produto"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    # Produtos relacionados (mesma categoria)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
        'page_title': product.name
    }
    
    return render(request, 'core/product_detail.html', context)


def category_view(request, slug):
    """View para produtos de uma categoria específica"""
    category = get_object_or_404(Category, slug=slug)
    
    products = Product.objects.filter(
        category=category,
        is_active=True
    )
    
    # Filtros e ordenação (similar ao product_list_view)
    search_query = request.GET.get('q')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort_by = request.GET.get('sort', 'name')
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass
    
    # Ordenação
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    elif sort_by == 'oldest':
        products = products.order_by('created_at')
    else:
        products = products.order_by('name')
    
    # Paginação
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
        'search_query': search_query,
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by,
        'page_title': f'Categoria: {category.name}'
    }
    
    return render(request, 'core/category.html', context)


@require_http_methods(["GET"])
def search_suggestions(request):
    """API para sugestões de busca"""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'suggestions': []})
    
    # Buscar produtos
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query),
        is_active=True
    )[:5]
    
    # Buscar categorias
    categories = Category.objects.filter(
        name__icontains=query,
        is_active=True
    )[:3]
    
    suggestions = []
    
    # Adicionar produtos
    for product in products:
        suggestions.append({
            'type': 'product',
            'name': product.name,
            'url': f'/produto/{product.slug}/',
            'image': product.get_main_image_url(),
            'price': str(product.price)
        })
    
    # Adicionar categorias
    for category in categories:
        suggestions.append({
            'type': 'category',
            'name': f'Categoria: {category.name}',
            'url': f'/categoria/{category.slug}/',
            'image': category.image.url if category.image else None
        })
    
    return JsonResponse({'suggestions': suggestions})


def about_view(request):
    """View da página sobre"""
    context = {
        'page_title': 'Sobre Nós'
    }
    return render(request, 'core/about.html', context)


def contact_view(request):
    """View da página de contato"""
    context = {
        'page_title': 'Contato'
    }
    return render(request, 'core/contact.html', context)


def privacy_view(request):
    """View da página de política de privacidade"""
    context = {
        'page_title': 'Política de Privacidade'
    }
    return render(request, 'core/privacy.html', context)


def terms_view(request):
    """View da página de termos de uso"""
    context = {
        'page_title': 'Termos de Uso'
    }
    return render(request, 'core/terms.html', context)
