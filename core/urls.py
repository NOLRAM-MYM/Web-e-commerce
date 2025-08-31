from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Página inicial
    path('', views.home_view, name='home'),
    
    # Produtos
    path('produtos/', views.product_list_view, name='product_list'),
    path('produto/<slug:slug>/', views.product_detail_view, name='product_detail'),
    
    # Categorias
    path('categoria/<slug:slug>/', views.category_view, name='category'),
    
    # Páginas institucionais
    path('sobre/', views.about_view, name='about'),
    path('contato/', views.contact_view, name='contact'),
    path('privacidade/', views.privacy_view, name='privacy'),
    path('termos/', views.terms_view, name='terms'),
    
    # APIs
    path('api/search-suggestions/', views.search_suggestions, name='search_suggestions'),
]