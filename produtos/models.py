from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
import os


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nome')
    description = models.TextField(blank=True, verbose_name='Descrição')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Product(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('JPY', 'Japanese Yen'),
        ('BRL', 'Brazilian Real'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='Nome')
    description = models.TextField(verbose_name='Descrição')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço')
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='BRL', verbose_name='Moeda')
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name='Quantidade em Estoque')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Categoria')
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['is_active']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('produto_detail', kwargs={'pk': self.pk})
    
    @property
    def is_in_stock(self):
        return self.stock_quantity > 0
    
    def get_main_image(self):
        """Retorna a primeira imagem do produto ou None"""
        return self.images.first()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='Produto')
    image = models.ImageField(upload_to='products/', verbose_name='Imagem')
    alt_text = models.CharField(max_length=200, blank=True, verbose_name='Texto Alternativo')
    is_main = models.BooleanField(default=False, verbose_name='Imagem Principal')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    
    class Meta:
        verbose_name = 'Imagem do Produto'
        verbose_name_plural = 'Imagens dos Produtos'
        ordering = ['-is_main', 'created_at']
    
    def __str__(self):
        return f'Imagem de {self.product.name}'
    
    def save(self, *args, **kwargs):
        # Se esta imagem for marcada como principal, desmarcar outras
        if self.is_main:
            ProductImage.objects.filter(product=self.product, is_main=True).update(is_main=False)
        
        super().save(*args, **kwargs)
        
        # Redimensionar imagem se necessário
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 800 or img.width > 800:
                output_size = (800, 800)
                img.thumbnail(output_size)
                img.save(self.image.path)
    
    def delete(self, *args, **kwargs):
        # Deletar arquivo físico quando o objeto for deletado
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)
