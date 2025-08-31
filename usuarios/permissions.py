from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from functools import wraps


def is_superadmin(user):
    """
    Verifica se o usuário é o superadministrador específico
    """
    return (
        user.is_authenticated and 
        user.is_superuser and 
        user.email == 'admin@sistema.com'
    )


def superadmin_required(function=None, redirect_field_name=None, login_url=None):
    """
    Decorator que requer que o usuário seja o superadministrador específico
    """
    actual_decorator = user_passes_test(
        is_superadmin,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


class SuperAdminMixin:
    """
    Mixin para views que requerem privilégios de superadministrador
    """
    def dispatch(self, request, *args, **kwargs):
        if not is_superadmin(request.user):
            raise PermissionDenied("Acesso restrito ao superadministrador")
        return super().dispatch(request, *args, **kwargs)


def create_admin_permissions():
    """
    Cria permissões customizadas para o sistema de administração
    """
    # Permissões para upload de imagens
    image_content_type, created = ContentType.objects.get_or_create(
        app_label='usuarios',
        model='imageupload'
    )
    
    permissions_to_create = [
        ('can_upload_images', 'Pode fazer upload de imagens'),
        ('can_manage_categories', 'Pode gerenciar categorias'),
        ('can_access_admin_panel', 'Pode acessar painel administrativo'),
        ('can_manage_users', 'Pode gerenciar usuários'),
        ('can_view_reports', 'Pode visualizar relatórios'),
        ('can_manage_orders', 'Pode gerenciar pedidos'),
        ('can_manage_products', 'Pode gerenciar produtos'),
        ('can_manage_system_settings', 'Pode gerenciar configurações do sistema'),
    ]
    
    created_permissions = []
    for codename, name in permissions_to_create:
        permission, created = Permission.objects.get_or_create(
            codename=codename,
            name=name,
            content_type=image_content_type
        )
        if created:
            created_permissions.append(permission)
    
    return created_permissions


def assign_superadmin_permissions(user):
    """
    Atribui todas as permissões necessárias ao superadministrador
    """
    if not is_superadmin(user):
        return False
    
    # Criar permissões se não existirem
    create_admin_permissions()
    
    # Atribuir todas as permissões ao superadministrador
    all_permissions = Permission.objects.all()
    user.user_permissions.set(all_permissions)
    
    return True


class AdminSecurityMiddleware:
    """
    Middleware para garantir segurança adicional no painel administrativo
    """
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Verificar se é uma requisição para o admin
        if request.path.startswith('/admin/'):
            # Permitir apenas para superadministrador ou staff autorizado
            if request.user.is_authenticated:
                if not (request.user.is_staff or is_superadmin(request.user)):
                    raise PermissionDenied("Acesso negado ao painel administrativo")
        
        response = self.get_response(request)
        return response


def check_image_upload_permission(user):
    """
    Verifica se o usuário tem permissão para upload de imagens
    """
    return (
        is_superadmin(user) or 
        user.has_perm('usuarios.can_upload_images')
    )


def check_category_management_permission(user):
    """
    Verifica se o usuário tem permissão para gerenciar categorias
    """
    return (
        is_superadmin(user) or 
        user.has_perm('usuarios.can_manage_categories')
    )