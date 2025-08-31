from django.urls import path
from . import views

app_name = 'produtos'

urlpatterns = [
    # Admin - Produtos
    path('admin/', views.product_admin_list, name='admin_list'),
    path('admin/criar/', views.product_admin_create, name='admin_create'),
    path('admin/editar/<int:product_id>/', views.product_admin_edit, name='admin_edit'),
    path('admin/deletar/<int:product_id>/', views.product_admin_delete, name='admin_delete'),
    
    # Admin - Categorias
    path('admin/categorias/', views.category_admin_list, name='category_admin_list'),
    path('admin/categorias/criar/', views.category_admin_create, name='category_admin_create'),
    path('admin/categorias/editar/<int:category_id>/', views.category_admin_edit, name='category_admin_edit'),
    path('admin/categorias/deletar/<int:category_id>/', views.category_admin_delete, name='category_admin_delete'),
    
    # APIs
    path('api/check-stock/<int:product_id>/', views.check_stock, name='check_stock'),
    path('api/upload-image/', views.upload_product_image, name='upload_image'),
]