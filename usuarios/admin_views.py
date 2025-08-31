from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from produtos.models import Category, Product, ProductImage
from usuarios.models import UserProfile
from usuarios.permissions import (
    superadmin_required, 
    SuperAdminMixin,
    check_image_upload_permission,
    check_category_management_permission
)
import json
import os


class SuperAdminDashboardView(SuperAdminMixin, TemplateView):
    """
    Dashboard principal do superadministrador
    """
    template_name = 'usuarios/superadmin_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estatísticas do sistema
        context.update({
            'total_users': User.objects.count(),
            'total_categories': Category.objects.count(),
            'total_products': Product.objects.count(),
            'total_images': ProductImage.objects.count(),
            'active_products': Product.objects.filter(is_active=True).count(),
            'recent_users': User.objects.order_by('-date_joined')[:5],
            'recent_products': Product.objects.order_by('-created_at')[:5],
        })
        
        return context


@superadmin_required
def upload_image_view(request):
    """
    View para upload de imagens de produtos pelo superadministrador.
    """
    if request.method == 'POST':
        try:
            product_id = request.POST.get('product')
            alt_text = request.POST.get('alt_text', '')
            is_main = request.POST.get('is_main') == 'on'
            image_file = request.FILES.get('image')
            
            if not product_id or not image_file:
                messages.error(request, 'Produto e imagem são obrigatórios.')
                return redirect('usuarios:upload_image')
            
            product = get_object_or_404(Product, id=product_id)
            
            # Criar nova imagem do produto
            product_image = ProductImage.objects.create(
                product=product,
                image=image_file,
                alt_text=alt_text,
                is_main=is_main
            )
            
            messages.success(request, f'Imagem enviada com sucesso para {product.name}!')
            return redirect('usuarios:upload_image')
            
        except Exception as e:
            messages.error(request, f'Erro ao enviar imagem: {str(e)}')
            return redirect('usuarios:upload_image')
    
    products = Product.objects.all().order_by('name')
    context = {
        'products': products,
        'title': 'Upload de Imagens'
    }
    return render(request, 'usuarios/upload_image.html', context)


@superadmin_required
def manage_categories_view(request):
    """
    View para gerenciamento de categorias pelo superadministrador.
    """
    if request.method == 'POST':
        try:
            action = request.POST.get('action')
            
            if action == 'create':
                name = request.POST.get('name', '').strip()
                description = request.POST.get('description', '').strip()
                
                if not name:
                    messages.error(request, 'Nome da categoria é obrigatório.')
                    return redirect('usuarios:manage_categories')
                
                if Category.objects.filter(name__iexact=name).exists():
                    messages.error(request, 'Já existe uma categoria com este nome.')
                    return redirect('usuarios:manage_categories')
                
                Category.objects.create(name=name, description=description)
                messages.success(request, f'Categoria "{name}" criada com sucesso!')
                
            elif action == 'edit':
                category_id = request.POST.get('category_id')
                name = request.POST.get('name', '').strip()
                description = request.POST.get('description', '').strip()
                
                if not name or not category_id:
                    messages.error(request, 'Dados inválidos para edição.')
                    return redirect('usuarios:manage_categories')
                
                category = get_object_or_404(Category, id=category_id)
                
                # Verificar se o novo nome já existe (exceto para a categoria atual)
                if Category.objects.filter(name__iexact=name).exclude(id=category_id).exists():
                    messages.error(request, 'Já existe uma categoria com este nome.')
                    return redirect('usuarios:manage_categories')
                
                category.name = name
                category.description = description
                category.save()
                messages.success(request, f'Categoria "{name}" atualizada com sucesso!')
                
            elif action == 'delete':
                category_id = request.POST.get('category_id')
                category = get_object_or_404(Category, id=category_id)
                
                # Verificar se a categoria tem produtos
                if category.products.exists():
                    messages.error(request, f'Não é possível excluir a categoria "{category.name}" pois ela possui produtos associados.')
                    return redirect('usuarios:manage_categories')
                
                category_name = category.name
                category.delete()
                messages.success(request, f'Categoria "{category_name}" excluída com sucesso!')
            
            return redirect('usuarios:manage_categories')
            
        except Exception as e:
            messages.error(request, f'Erro ao processar solicitação: {str(e)}')
            return redirect('usuarios:manage_categories')
    
    categories = Category.objects.annotate(product_count=Count('products')).order_by('name')
    context = {
        'categories': categories,
        'title': 'Gerenciar Categorias'
    }
    return render(request, 'usuarios/manage_categories.html', context)


@superadmin_required
def system_users_view(request):
    """
    View para gerenciamento de usuários do sistema
    """
    # Filtros
    search = request.GET.get('search', '')
    status = request.GET.get('status', '')
    order = request.GET.get('order', '-date_joined')
    
    users = User.objects.all()
    
    # Aplicar filtros
    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )
    
    if status == 'active':
        users = users.filter(is_active=True)
    elif status == 'inactive':
        users = users.filter(is_active=False)
    elif status == 'superuser':
        users = users.filter(is_superuser=True)
    
    # Ordenação
    users = users.order_by(order)
    
    # Estatísticas
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    inactive_users = User.objects.filter(is_active=False).count()
    superusers = User.objects.filter(is_superuser=True).count()
    
    context = {
        'users': users,
        'total_users': total_users,
        'active_users': active_users,
        'inactive_users': inactive_users,
        'superusers': superusers,
        'search': search,
        'status': status,
        'order': order,
    }
    
    return render(request, 'usuarios/system_users.html', context)


@superadmin_required
@require_http_methods(["POST"])
def toggle_user_status(request, user_id):
    """
    Ativar/desativar usuário
    """
    user = get_object_or_404(User, id=user_id)
    
    # Não permitir desativar o próprio superadministrador
    if user.email == 'admin@sistema.com':
        return JsonResponse({
            'success': False,
            'message': 'Não é possível desativar o superadministrador.'
        })
    
    user.is_active = not user.is_active
    user.save()
    
    status = 'ativado' if user.is_active else 'desativado'
    
    return JsonResponse({
        'success': True,
        'message': f'Usuário {user.username} {status} com sucesso.',
        'is_active': user.is_active
    })


@superadmin_required
def system_reports_view(request):
    """
    View para relatórios do sistema
    """
    # Estatísticas detalhadas
    stats = {
        'users': {
            'total': User.objects.count(),
            'active': User.objects.filter(is_active=True).count(),
            'staff': User.objects.filter(is_staff=True).count(),
            'superusers': User.objects.filter(is_superuser=True).count(),
        },
        'products': {
            'total': Product.objects.count(),
            'active': Product.objects.filter(is_active=True).count(),
            'with_images': Product.objects.filter(productimage__isnull=False).distinct().count(),
        },
        'categories': {
            'total': Category.objects.count(),
            'with_products': Category.objects.filter(product__isnull=False).distinct().count(),
        },
        'images': {
            'total': ProductImage.objects.count(),
            'primary': ProductImage.objects.filter(is_primary=True).count(),
        }
    }
    
    return render(request, 'usuarios/system_reports.html', {
        'stats': stats
    })