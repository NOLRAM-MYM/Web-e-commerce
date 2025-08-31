from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, PasswordResetToken
from django.utils.html import format_html


class UserProfileInline(admin.StackedInline):
    """Inline para editar perfil do usuário junto com o usuário"""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Perfil do Usuário'
    fields = (
        'phone', 'birth_date', 'avatar',
        'address', 'city', 'state', 'zip_code', 'country',
        'preferred_currency', 'email_notifications', 'marketing_emails'
    )


class UserAdmin(BaseUserAdmin):
    """Administração customizada para usuários com perfil integrado"""
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Administração para perfis de usuário"""
    list_display = ('user', 'phone', 'city', 'state', 'created_at')
    list_filter = ('country', 'preferred_currency', 'email_notifications', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone', 'city')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Usuário', {
            'fields': ('user',)
        }),
        ('Informações Pessoais', {
            'fields': ('phone', 'birth_date', 'avatar')
        }),
        ('Endereço', {
            'fields': ('address', 'city', 'state', 'zip_code', 'country')
        }),
        ('Preferências', {
            'fields': ('preferred_currency', 'email_notifications', 'marketing_emails')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.avatar.url)
        return "Sem avatar"
    avatar_preview.short_description = 'Avatar'


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    """Administração para tokens de recuperação de senha"""
    list_display = ('user', 'token', 'created_at', 'used', 'is_valid_status')
    list_filter = ('used', 'created_at')
    search_fields = ('user__username', 'user__email', 'token')
    readonly_fields = ('token', 'created_at')
    
    def is_valid_status(self, obj):
        return obj.is_valid()
    is_valid_status.boolean = True
    is_valid_status.short_description = 'Válido'
    
    def has_add_permission(self, request):
        return False  # Não permitir criação manual de tokens


# Re-registrar o modelo User com a nova configuração
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Customizar títulos do admin
admin.site.site_header = 'Administração do E-commerce'
admin.site.site_title = 'Admin E-commerce'
admin.site.index_title = 'Painel de Controle'
