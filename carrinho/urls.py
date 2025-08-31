from django.urls import path
from . import views

app_name = 'carrinho'

urlpatterns = [
    # Carrinho
    path('', views.cart_view, name='cart'),
    path('adicionar/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remover/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('atualizar/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('limpar/', views.clear_cart, name='clear_cart'),
    
    # APIs AJAX
    path('api/count/', views.cart_count, name='cart_count'),
    path('api/total/', views.cart_total, name='cart_total'),
]