from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
import os


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Usuário')
    
    # Informações pessoais
    phone = models.CharField(max_length=20, blank=True, verbose_name='Telefone')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Data de Nascimento')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Avatar')
    
    # Endereço padrão
    address = models.TextField(blank=True, verbose_name='Endereço')
    city = models.CharField(max_length=100, blank=True, verbose_name='Cidade')
    state = models.CharField(max_length=100, blank=True, verbose_name='Estado')
    zip_code = models.CharField(max_length=20, blank=True, verbose_name='CEP')
    country = models.CharField(max_length=100, default='Brasil', verbose_name='País')
    
    # Preferências
    preferred_currency = models.CharField(
        max_length=3,
        choices=[
            ('USD', 'US Dollar'),
            ('JPY', 'Japanese Yen'),
            ('BRL', 'Brazilian Real'),
        ],
        default='BRL',
        verbose_name='Moeda Preferida'
    )
    
    # Configurações de notificação
    email_notifications = models.BooleanField(default=True, verbose_name='Notificações por Email')
    marketing_emails = models.BooleanField(default=False, verbose_name='Emails de Marketing')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        verbose_name = 'Perfil do Usuário'
        verbose_name_plural = 'Perfis dos Usuários'
    
    def __str__(self):
        return f'Perfil de {self.user.username}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Redimensionar avatar se necessário
        if self.avatar:
            img = Image.open(self.avatar.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.avatar.path)
    
    def delete(self, *args, **kwargs):
        # Deletar arquivo de avatar quando o perfil for deletado
        if self.avatar and os.path.isfile(self.avatar.path):
            os.remove(self.avatar.path)
        super().delete(*args, **kwargs)
    
    @property
    def full_name(self):
        """Retorna o nome completo do usuário"""
        return f'{self.user.first_name} {self.user.last_name}'.strip() or self.user.username
    
    @property
    def has_complete_address(self):
        """Verifica se o usuário tem um endereço completo"""
        return all([self.address, self.city, self.state, self.zip_code])


class PasswordResetToken(models.Model):
    """Modelo para tokens de recuperação de senha personalizados"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    token = models.CharField(max_length=100, unique=True, verbose_name='Token')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    used = models.BooleanField(default=False, verbose_name='Usado')
    
    class Meta:
        verbose_name = 'Token de Recuperação de Senha'
        verbose_name_plural = 'Tokens de Recuperação de Senha'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Token para {self.user.username}'
    
    def is_valid(self):
        """Verifica se o token ainda é válido (24 horas)"""
        from django.utils import timezone
        from datetime import timedelta
        
        if self.used:
            return False
        
        expiry_time = self.created_at + timedelta(hours=24)
        return timezone.now() < expiry_time
    
    def mark_as_used(self):
        """Marca o token como usado"""
        self.used = True
        self.save()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Cria automaticamente um perfil quando um usuário é criado"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Salva o perfil quando o usuário é salvo"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
