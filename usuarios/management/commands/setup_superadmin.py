from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from usuarios.permissions import (
    create_admin_permissions, 
    assign_superadmin_permissions,
    is_superadmin
)
from django.db import transaction


class Command(BaseCommand):
    help = 'Configura o superadministrador com todas as permissões necessárias'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            default='admin@sistema.com',
            help='Email do superadministrador (padrão: admin@sistema.com)'
        )
        parser.add_argument(
            '--username',
            type=str,
            default='admin',
            help='Username do superadministrador (padrão: admin)'
        )
    
    def handle(self, *args, **options):
        email = options['email']
        username = options['username']
        
        try:
            with transaction.atomic():
                # Buscar ou criar o superadministrador
                user, created = User.objects.get_or_create(
                    email=email,
                    defaults={
                        'username': username,
                        'is_staff': True,
                        'is_superuser': True,
                        'is_active': True,
                        'first_name': 'Super',
                        'last_name': 'Administrador'
                    }
                )
                
                if not created:
                    # Atualizar usuário existente
                    user.username = username
                    user.is_staff = True
                    user.is_superuser = True
                    user.is_active = True
                    user.save()
                    self.stdout.write(
                        self.style.WARNING(f'Usuário {email} já existia. Atualizando permissões...')
                    )
                else:
                    self.stdout.write(
                        self.style.SUCCESS(f'Superadministrador {email} criado com sucesso!')
                    )
                
                # Criar permissões customizadas
                self.stdout.write('Criando permissões customizadas...')
                created_permissions = create_admin_permissions()
                
                if created_permissions:
                    self.stdout.write(
                        self.style.SUCCESS(f'{len(created_permissions)} permissões criadas.')
                    )
                else:
                    self.stdout.write('Permissões já existiam.')
                
                # Atribuir todas as permissões ao superadministrador
                self.stdout.write('Atribuindo permissões ao superadministrador...')
                success = assign_superadmin_permissions(user)
                
                if success:
                    self.stdout.write(
                        self.style.SUCCESS('Todas as permissões foram atribuídas com sucesso!')
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR('Erro ao atribuir permissões.')
                    )
                
                # Verificar se o usuário é reconhecido como superadmin
                if is_superadmin(user):
                    self.stdout.write(
                        self.style.SUCCESS('✓ Superadministrador configurado corretamente!')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING('⚠ Usuário criado mas não reconhecido como superadmin.')
                    )
                
                # Exibir informações de acesso
                self.stdout.write('\n' + '='*50)
                self.stdout.write(self.style.SUCCESS('INFORMAÇÕES DE ACESSO:'))
                self.stdout.write(f'Email: {user.email}')
                self.stdout.write(f'Username: {user.username}')
                self.stdout.write('Senha: admin123 (conforme especificado)')
                self.stdout.write('URL Admin: http://localhost:8000/admin/')
                self.stdout.write('='*50)
                
                # Exibir funcionalidades disponíveis
                self.stdout.write('\n' + self.style.SUCCESS('FUNCIONALIDADES DISPONÍVEIS:'))
                self.stdout.write('✓ Upload de imagens com controle de permissões')
                self.stdout.write('✓ Registro e gerenciamento de categorias')
                self.stdout.write('✓ Acesso privilegiado a todas as áreas do sistema')
                self.stdout.write('✓ Gerenciamento completo de usuários')
                self.stdout.write('✓ Gerenciamento de produtos e imagens')
                self.stdout.write('✓ Controle total do sistema')
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erro ao configurar superadministrador: {str(e)}')
            )
            raise e