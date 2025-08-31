from django.contrib import admin
from .models import Category, Product, ProductImage
from django.utils.html import format_html
from django.db import models
from django.forms import CheckboxSelectMultiple


class ProductImageInline(admin.TabularInline):
    """Inline para gerenciar imagens dos produtos"""
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text', 'is_main')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover;" />', obj.image.url)
        return "Sem imagem"
    image_preview.short_description = 'Preview'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Administração para categorias de produtos"""
    list_display = ('name', 'description', 'product_count', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'description')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Qtd. Produtos'
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('products')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Administração para produtos"""
    inlines = [ProductImageInline]
    list_display = ('name', 'category', 'price_display', 'stock_quantity', 'is_active', 'main_image_preview', 'created_at')
    list_filter = ('category', 'currency', 'is_active', 'created_at')
    search_fields = ('name', 'description', 'category__name')
    list_editable = ('is_active', 'stock_quantity')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'description', 'category')
        }),
        ('Preço e Estoque', {
            'fields': ('price', 'currency', 'stock_quantity')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def price_display(self, obj):
        currency_symbols = {
            'USD': '$',
            'JPY': '¥',
            'BRL': 'R$'
        }
        symbol = currency_symbols.get(obj.currency, obj.currency)
        return f'{symbol} {obj.price}'
    price_display.short_description = 'Preço'
    price_display.admin_order_field = 'price'
    
    def main_image_preview(self, obj):
        main_image = obj.get_main_image()
        if main_image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />', main_image.image.url)
        return "Sem imagem"
    main_image_preview.short_description = 'Imagem'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category').prefetch_related('images')
    
    # Ações personalizadas
    actions = ['activate_products', 'deactivate_products', 'mark_out_of_stock']
    
    def activate_products(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} produtos foram ativados.')
    activate_products.short_description = 'Ativar produtos selecionados'
    
    def deactivate_products(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} produtos foram desativados.')
    deactivate_products.short_description = 'Desativar produtos selecionados'
    
    def mark_out_of_stock(self, request, queryset):
        updated = queryset.update(stock_quantity=0)
        self.message_user(request, f'{updated} produtos foram marcados como fora de estoque.')
    mark_out_of_stock.short_description = 'Marcar como fora de estoque'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """Administração para imagens de produtos"""
    list_display = ('product', 'image_preview', 'alt_text', 'is_main', 'created_at')
    list_filter = ('is_main', 'created_at', 'product__category')
    search_fields = ('product__name', 'alt_text')
    readonly_fields = ('created_at', 'image_preview_large')
    
    fieldsets = (
        ('Produto', {
            'fields': ('product',)
        }),
        ('Imagem', {
            'fields': ('image', 'image_preview_large', 'alt_text', 'is_main')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return "Sem imagem"
    image_preview.short_description = 'Preview'
    
    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="200" height="200" style="object-fit: cover; border-radius: 8px;" />', obj.image.url)
        return "Sem imagem"
    image_preview_large.short_description = 'Preview da Imagem'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('product')
