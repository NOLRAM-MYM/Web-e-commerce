from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    # Pedidos
    path('', views.order_list_view, name='order_list'),
    path('<str:order_number>/', views.order_detail_view, name='order_detail'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('checkout/success/', views.checkout_success_view, name='checkout_success'),
    path('checkout/cancel/', views.checkout_cancel_view, name='checkout_cancel'),
    
    # PayPal
    path('paypal/create-payment/', views.create_paypal_payment, name='create_paypal_payment'),
    path('paypal/execute-payment/', views.execute_paypal_payment, name='execute_paypal_payment'),
    path('paypal/webhook/', views.paypal_webhook, name='paypal_webhook'),
    
    # APIs
    path('api/cancel/<str:order_number>/', views.cancel_order, name='cancel_order'),
]