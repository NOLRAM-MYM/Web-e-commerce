from django import forms
from django.core.exceptions import ValidationError
from .models import Product, Category, ProductImage
from decimal import Decimal


class CategoryForm(forms.ModelForm):
    """Formulário para categoria"""
    
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da categoria'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descrição da categoria'
            })
        }
        labels = {
            'name': 'Nome',
            'description': 'Descrição'
        }
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            # Verificar se já existe uma categoria com este nome (exceto a atual)
            existing = Category.objects.filter(name__iexact=name)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            
            if existing.exists():
                raise ValidationError('Já existe uma categoria com este nome.')
        
        return name
    



class ProductForm(forms.ModelForm):
    """Formulário para produto"""
    
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'price', 'stock_quantity', 
            'category', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do produto'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descrição detalhada do produto'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'stock_quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'name': 'Nome',
            'description': 'Descrição',
            'price': 'Preço',
            'stock_quantity': 'Quantidade em Estoque',
            'category': 'Categoria',
            'is_active': 'Ativo'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar apenas categorias ativas
        self.fields['category'].queryset = Category.objects.all()
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            # Verificar se já existe um produto com este nome (exceto o atual)
            existing = Product.objects.filter(name__iexact=name)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            
            if existing.exists():
                raise ValidationError('Já existe um produto com este nome.')
        
        return name
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None:
            if price < Decimal('0.01'):
                raise ValidationError('O preço deve ser maior que zero.')
            if price > Decimal('999999.99'):
                raise ValidationError('Preço muito alto.')
        
        return price
    
    def clean_stock_quantity(self):
        stock = self.cleaned_data.get('stock_quantity')
        if stock is not None and stock < 0:
            raise ValidationError('A quantidade em estoque não pode ser negativa.')
        
        return stock
    



class ProductImageForm(forms.ModelForm):
    """Formulário para imagens adicionais do produto"""
    
    class Meta:
        model = ProductImage
        fields = ['image', 'alt_text', 'is_main']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'alt_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Texto alternativo para a imagem'
            }),
            'is_main': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'image': 'Imagem',
            'alt_text': 'Texto Alternativo',
            'is_main': 'Imagem Principal'
        }
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Validar tamanho do arquivo (5MB max)
            if image.size > 5 * 1024 * 1024:
                raise ValidationError('Imagem muito grande. Tamanho máximo: 5MB')
            
            # Validar tipo de arquivo
            allowed_types = ['image/jpeg', 'image/png', 'image/webp']
            if hasattr(image, 'content_type') and image.content_type not in allowed_types:
                raise ValidationError('Tipo de arquivo não permitido. Use JPEG, PNG ou WebP.')
        
        return image
    
    def clean(self):
        cleaned_data = super().clean()
        is_primary = cleaned_data.get('is_primary')
        
        # Se esta imagem for marcada como principal, verificar se já existe uma principal
        if is_primary and hasattr(self, 'instance') and self.instance.product:
            existing_primary = ProductImage.objects.filter(
                product=self.instance.product,
                is_primary=True
            )
            if self.instance.pk:
                existing_primary = existing_primary.exclude(pk=self.instance.pk)
            
            if existing_primary.exists():
                raise ValidationError('Já existe uma imagem principal para este produto.')
        
        return cleaned_data


class ProductSearchForm(forms.Form):
    """Formulário de busca de produtos"""
    
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar produtos...',
            'autocomplete': 'off'
        })
    )
    
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label='Todas as categorias',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    min_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Preço mínimo',
            'step': '0.01',
            'min': '0'
        })
    )
    
    max_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Preço máximo',
            'step': '0.01',
            'min': '0'
        })
    )
    
    sort_by = forms.ChoiceField(
        choices=[
            ('name', 'Nome A-Z'),
            ('-name', 'Nome Z-A'),
            ('price', 'Menor preço'),
            ('-price', 'Maior preço'),
            ('-created_at', 'Mais recentes'),
            ('created_at', 'Mais antigos'),
        ],
        required=False,
        initial='-created_at',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        min_price = cleaned_data.get('min_price')
        max_price = cleaned_data.get('max_price')
        
        if min_price and max_price and min_price > max_price:
            raise ValidationError('O preço mínimo não pode ser maior que o preço máximo.')