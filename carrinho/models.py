from django.db import models
from django.contrib.auth.models import User
from produtos.models import Product
from django.core.validators import MinValueValidator


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items', verbose_name='Usuário')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Produto')
    quantity = models.PositiveIntegerField(
        default=1, 
        validators=[MinValueValidator(1)],
        verbose_name='Quantidade'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Adicionado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        verbose_name = 'Item do Carrinho'
        verbose_name_plural = 'Itens do Carrinho'
        unique_together = ['user', 'product']
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['product']),
        ]
    
    def __str__(self):
        return f'{self.quantity}x {self.product.name} - {self.user.username}'
    
    @property
    def total_price(self):
        """Calcula o preço total do item (quantidade * preço unitário)"""
        return self.quantity * self.product.price
    
    def clean(self):
        """Validação personalizada"""
        from django.core.exceptions import ValidationError
        
        if self.product and not self.product.is_active:
            raise ValidationError('Não é possível adicionar um produto inativo ao carrinho.')
        
        if self.product and self.quantity > self.product.stock_quantity:
            raise ValidationError(
                f'Quantidade solicitada ({self.quantity}) excede o estoque disponível ({self.product.stock_quantity}).'
            )
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Cart(models.Model):
    """Modelo para representar o carrinho como um todo (opcional, para funcionalidades futuras)"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart', verbose_name='Usuário')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        verbose_name = 'Carrinho'
        verbose_name_plural = 'Carrinhos'
    
    def __str__(self):
        return f'Carrinho de {self.user.username}'
    
    @property
    def total_items(self):
        """Retorna o número total de itens no carrinho"""
        return self.user.cart_items.aggregate(
            total=models.Sum('quantity')
        )['total'] or 0
    
    @property
    def total_price(self):
        """Calcula o preço total do carrinho"""
        total = 0
        for item in self.user.cart_items.all():
            total += item.total_price
        return total
    
    @property
    def is_empty(self):
        """Verifica se o carrinho está vazio"""
        return not self.user.cart_items.exists()
    
    def clear(self):
        """Remove todos os itens do carrinho"""
        self.user.cart_items.all().delete()
