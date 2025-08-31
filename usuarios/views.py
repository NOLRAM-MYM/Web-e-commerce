from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import UserProfile, PasswordResetToken
from .forms import UserRegistrationForm, UserLoginForm, PasswordResetForm, PasswordResetConfirmForm


def register_view(request):
    """View para registro de usuário"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Conta criada com sucesso! Você pode fazer login agora.')
            return redirect('usuarios:login')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'usuarios/register.html', {'form': form})


def login_view(request):
    """View para login de usuário"""
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'core:home')
                messages.success(request, f'Bem-vindo, {user.first_name or user.username}!')
                return redirect(next_url)
            else:
                messages.error(request, 'Credenciais inválidas.')
    else:
        form = UserLoginForm()
    
    return render(request, 'usuarios/login.html', {'form': form})


@login_required
def logout_view(request):
    """View para logout de usuário"""
    logout(request)
    messages.success(request, 'Você foi desconectado com sucesso.')
    return redirect('core:home')


@login_required
def profile_view(request):
    """View para visualizar e editar perfil do usuário"""
    profile = request.user.userprofile
    
    if request.method == 'POST':
        # Atualizar dados do usuário
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        
        # Atualizar dados do perfil
        profile.phone = request.POST.get('phone', '')
        profile.birth_date = request.POST.get('birth_date') or None
        profile.address = request.POST.get('address', '')
        profile.city = request.POST.get('city', '')
        profile.state = request.POST.get('state', '')
        profile.zip_code = request.POST.get('zip_code', '')
        profile.country = request.POST.get('country', '')
        profile.preferred_currency = request.POST.get('preferred_currency', 'USD')
        profile.email_notifications = 'email_notifications' in request.POST
        profile.marketing_emails = 'marketing_emails' in request.POST
        
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        
        profile.save()
        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('usuarios:profile')
    
    return render(request, 'usuarios/profile.html', {
        'user': request.user,
        'profile': profile
    })


def password_reset_request(request):
    """View para solicitar redefinição de senha"""
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                
                # Criar token de redefinição
                token = get_random_string(32)
                reset_token = PasswordResetToken.objects.create(
                    user=user,
                    token=token
                )
                
                # Enviar email
                reset_url = request.build_absolute_uri(
                    reverse('usuarios:password_reset_confirm', args=[token])
                )
                
                subject = 'Redefinição de Senha - E-commerce'
                message = f'''
Olá {user.first_name or user.username},

Você solicitou a redefinição de sua senha.
Clique no link abaixo para redefinir sua senha:

{reset_url}

Este link expira em 1 hora.

Se você não solicitou esta redefinição, ignore este email.

Atenciosamente,
Equipe E-commerce
                '''
                
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                
                messages.success(request, 'Email de redefinição enviado! Verifique sua caixa de entrada.')
                return redirect('usuarios:login')
                
            except User.DoesNotExist:
                messages.error(request, 'Nenhum usuário encontrado com este email.')
    else:
        form = PasswordResetForm()
    
    return render(request, 'usuarios/password_reset_request.html', {'form': form})


def password_reset_confirm(request, token):
    """View para confirmar redefinição de senha"""
    try:
        reset_token = PasswordResetToken.objects.get(token=token)
        if not reset_token.is_valid():
            messages.error(request, 'Token inválido ou expirado.')
            return redirect('usuarios:password_reset_request')
    except PasswordResetToken.DoesNotExist:
        messages.error(request, 'Token inválido.')
        return redirect('usuarios:password_reset_request')
    
    if request.method == 'POST':
        form = PasswordResetConfirmForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = reset_token.user
            user.set_password(password)
            user.save()
            
            reset_token.mark_as_used()
            
            messages.success(request, 'Senha redefinida com sucesso! Você pode fazer login agora.')
            return redirect('usuarios:login')
    else:
        form = PasswordResetConfirmForm()
    
    return render(request, 'usuarios/password_reset_confirm.html', {
        'form': form,
        'token': token
    })


@csrf_exempt
@require_http_methods(["POST"])
def check_username_availability(request):
    """API para verificar disponibilidade de username"""
    data = json.loads(request.body)
    username = data.get('username', '')
    
    if len(username) < 3:
        return JsonResponse({
            'available': False,
            'message': 'Username deve ter pelo menos 3 caracteres.'
        })
    
    exists = User.objects.filter(username=username).exists()
    return JsonResponse({
        'available': not exists,
        'message': 'Username disponível!' if not exists else 'Username já está em uso.'
    })


@csrf_exempt
@require_http_methods(["POST"])
def check_email_availability(request):
    """API para verificar disponibilidade de email"""
    data = json.loads(request.body)
    email = data.get('email', '')
    
    exists = User.objects.filter(email=email).exists()
    return JsonResponse({
        'available': not exists,
        'message': 'Email disponível!' if not exists else 'Email já está em uso.'
    })
