from django.db import models
from django.contrib.auth.models import User
from produtos.models import Product
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('processing', 'Processando'),
        ('shipped', 'Enviado'),
        ('delivered', 'Entregue'),
        ('cancelled', 'Cancelado'),
        ('refunded', 'Reembolsado'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('completed', 'Concluído'),
        ('failed', 'Falhou'),
        ('cancelled', 'Cancelado'),
        ('refunded', 'Reembolsado'),
    ]
    
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('JPY', 'Japanese Yen'),
        ('BRL', 'Brazilian Real'),
    ]
    
    # Identificação
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.CharField(max_length=20, unique=True, verbose_name='Número do Pedido')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='Usuário')
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Status')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending', verbose_name='Status do Pagamento')
    
    # Valores
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor Total')
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='BRL', verbose_name='Moeda')
    
    # Informações de entrega
    shipping_address = models.TextField(verbose_name='Endereço de Entrega')
    shipping_city = models.CharField(max_length=100, verbose_name='Cidade')
    shipping_state = models.CharField(max_length=100, verbose_name='Estado')
    shipping_zip_code = models.CharField(max_length=20, verbose_name='CEP')
    shipping_country = models.CharField(max_length=100, default='Brasil', verbose_name='País')
    
    # Informações de pagamento
    payment_method = models.CharField(max_length=50, default='paypal', verbose_name='Método de Pagamento')
    payment_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='ID do Pagamento')
    paypal_order_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='ID do Pedido PayPal')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    shipped_at = models.DateTimeField(null=True, blank=True, verbose_name='Enviado em')
    delivered_at = models.DateTimeField(null=True, blank=True, verbose_name='Entregue em')
    
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['status']),
            models.Index(fields=['payment_status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['order_number']),
        ]
    
    def __str__(self):
        return f'Pedido {self.order_number} - {self.user.username}'
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            # Gerar número do pedido único
            import random
            import string
            while True:
                order_number = ''.join(random.choices(string.digits, k=10))
                if not Order.objects.filter(order_number=order_number).exists():
                    self.order_number = order_number
                    break
        super().save(*args, **kwargs)
    
    @property
    def total_items(self):
        """Retorna o número total de itens no pedido"""
        return self.items.aggregate(
            total=models.Sum('quantity')
        )['total'] or 0
    
    def can_be_cancelled(self):
        """Verifica se o pedido pode ser cancelado"""
        return self.status in ['pending', 'processing']
    
    def can_be_refunded(self):
        """Verifica se o pedido pode ser reembolsado"""
        return self.payment_status == 'completed' and self.status in ['delivered', 'shipped']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Pedido')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Produto')
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Quantidade'
    )
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço Unitário')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço Total')
    
    # Snapshot dos dados do produto no momento da compra
    product_name = models.CharField(max_length=200, verbose_name='Nome do Produto')
    product_description = models.TextField(blank=True, verbose_name='Descrição do Produto')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    
    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['product']),
        ]
    
    def __str__(self):
        return f'{self.quantity}x {self.product_name} - Pedido {self.order.order_number}'
    
    def save(self, *args, **kwargs):
        # Calcular preço total automaticamente
        self.total_price = self.quantity * self.unit_price
        
        # Salvar snapshot dos dados do produto
        if self.product:
            self.product_name = self.product.name
            self.product_description = self.product.description
            if not self.unit_price:
                self.unit_price = self.product.price
        
        super().save(*args, **kwargs)
