# 🛒 Web Commerce - Sistema de E-commerce Completo

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2.5-green.svg)
![Magic UI](https://img.shields.io/badge/Magic%20UI-Latest-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

Um sistema de e-commerce moderno e completo desenvolvido com Django, featuring uma interface elegante com Magic UI e funcionalidades avançadas de administração.

## 📋 Índice

- [Características](#-características)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Uso](#-uso)
- [Funcionalidades](#-funcionalidades)
- [API Endpoints](#-api-endpoints)
- [Administração](#-administração)
- [Contribuição](#-contribuição)
- [Licença](#-licença)

## ✨ Características

- **Interface Moderna**: Design responsivo com Magic UI components
- **Sistema de Autenticação Completo**: Login, registro, recuperação de senha
- **Gestão de Produtos**: CRUD completo com categorias e imagens
- **Carrinho de Compras**: Sistema de carrinho persistente
- **Sistema de Pedidos**: Gestão completa de pedidos com status
- **Integração PayPal**: Pagamentos seguros via PayPal
- **Painel Administrativo**: Dashboard completo para superadministradores
- **Multi-moeda**: Suporte para USD, JPY e BRL
- **Sistema de Notificações**: Emails automáticos e notificações
- **Segurança Avançada**: Middleware de segurança personalizado

## 🚀 Tecnologias Utilizadas

### Backend
- **Django 5.2.5** - Framework web principal
- **Django REST Framework 3.16.1** - API REST
- **SQLite** - Banco de dados (desenvolvimento)
- **PostgreSQL** - Banco de dados (produção)
- **Pillow 11.3.0** - Processamento de imagens
- **PayPal REST SDK 1.13.3** - Integração de pagamentos

### Frontend
- **Magic UI** - Biblioteca de componentes UI
- **HTML5/CSS3** - Estrutura e estilização
- **JavaScript** - Interatividade
- **Font Awesome** - Ícones

### Ferramentas
- **Python Decouple** - Gerenciamento de configurações
- **BCrypt** - Criptografia de senhas
- **UV** - Gerenciador de dependências

## 📁 Estrutura do Projeto

```
web_commerce/
├── 📁 ecommerce_project/          # Configurações principais do Django
│   ├── settings.py                # Configurações do projeto
│   ├── urls.py                   # URLs principais
│   └── wsgi.py                   # Configuração WSGI
├── 📁 core/                      # App principal (home, produtos)
│   ├── models.py                 # Modelos principais
│   ├── views.py                  # Views do core
│   └── urls.py                   # URLs do core
├── 📁 usuarios/                  # Sistema de usuários
│   ├── models.py                 # UserProfile, PasswordResetToken
│   ├── views.py                  # Autenticação e perfil
│   ├── admin_views.py            # Views administrativas
│   └── permissions.py            # Middleware de segurança
├── 📁 produtos/                  # Gestão de produtos
│   ├── models.py                 # Product, Category, ProductImage
│   ├── views.py                  # CRUD de produtos
│   └── forms.py                  # Formulários de produtos
├── 📁 carrinho/                  # Sistema de carrinho
│   ├── models.py                 # CartItem, Cart
│   └── views.py                  # Gestão do carrinho
├── 📁 pedidos/                   # Sistema de pedidos
│   ├── models.py                 # Order, OrderItem
│   └── views.py                  # Processamento de pedidos
├── 📁 static/                    # Arquivos estáticos
│   ├── 📁 css/                   # Estilos CSS
│   │   ├── magic-ui-fixes.css    # Correções Magic UI
│   │   ├── navbar-dropdown-fix.css # Correções navbar
│   │   └── input-text-color-fix.css # Correções de inputs
│   └── 📁 js/                    # Scripts JavaScript
│       ├── magic-ui-components.js # Componentes Magic UI
│       └── navbar-active-states.js # Estados ativos navbar
├── 📁 templates/                 # Templates HTML
│   ├── base.html                 # Template base
│   ├── 📁 core/                  # Templates do core
│   ├── 📁 usuarios/              # Templates de usuários
│   ├── 📁 carrinho/              # Templates do carrinho
│   └── 📁 pedidos/               # Templates de pedidos
├── 📁 media/                     # Arquivos de mídia
├── db.sqlite3                    # Banco de dados SQLite
├── pyproject.toml               # Configuração do projeto
└── README.md                    # Este arquivo
```

## 🔧 Instalação

### Pré-requisitos
- Python 3.12+
- UV (gerenciador de dependências)
- Git

### Passo a passo

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/web-commerce.git
cd web-commerce
```

2. **Instale as dependências**
```bash
uv sync
```

3. **Ative o ambiente virtual**
```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

4. **Configure as variáveis de ambiente**
```bash
cp .env.example .env
```

5. **Execute as migrações**
```bash
python manage.py migrate
```

6. **Crie o superusuário**
```bash
python manage.py createsuperuser
```

7. **Inicie o servidor**
```bash
python manage.py runserver
```

## ⚙️ Configuração

### Variáveis de Ambiente (.env)

```env
# Django
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# PayPal
PAYPAL_CLIENT_ID=seu-paypal-client-id
PAYPAL_CLIENT_SECRET=seu-paypal-client-secret
PAYPAL_MODE=sandbox  # ou 'live' para produção

# Email
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-de-app

# Segurança
USE_HTTPS=False
SECURE_COOKIES=False
```

### Configurações de Produção

Para produção, ajuste as seguintes configurações:

```env
DEBUG=False
USE_HTTPS=True
SECURE_COOKIES=True
PAYPAL_MODE=live
```

## 🎯 Uso

### Acesso ao Sistema

- **Site Principal**: http://localhost:8000/
- **Admin Django**: http://localhost:8000/admin/
- **Dashboard Admin**: http://localhost:8000/usuarios/superadmin/

### Credenciais Padrão

**Superadministrador**:
- Email: admin@sistema.com
- Senha: admin123

## 🔥 Funcionalidades

### 👤 Sistema de Usuários
- ✅ Registro de usuários com validação
- ✅ Login/Logout seguro
- ✅ Recuperação de senha por email
- ✅ Perfil de usuário completo
- ✅ Upload de avatar
- ✅ Preferências de moeda
- ✅ Configurações de notificação

### 🛍️ Gestão de Produtos
- ✅ CRUD completo de produtos
- ✅ Sistema de categorias
- ✅ Upload múltiplo de imagens
- ✅ Controle de estoque
- ✅ Suporte multi-moeda
- ✅ Produtos ativos/inativos
- ✅ Busca e filtros avançados

### 🛒 Carrinho de Compras
- ✅ Adicionar/remover produtos
- ✅ Atualizar quantidades
- ✅ Carrinho persistente
- ✅ Validação de estoque
- ✅ Cálculo automático de totais

### 📦 Sistema de Pedidos
- ✅ Checkout completo
- ✅ Múltiplos status de pedido
- ✅ Integração PayPal
- ✅ Histórico de pedidos
- ✅ Rastreamento de entrega
- ✅ Sistema de reembolso

### 🔐 Administração
- ✅ Dashboard administrativo
- ✅ Gestão de usuários
- ✅ Relatórios do sistema
- ✅ Upload de imagens
- ✅ Gestão de categorias
- ✅ Controle de permissões

### 🎨 Interface
- ✅ Design responsivo
- ✅ Magic UI components
- ✅ Navbar interativa
- ✅ Estados ativos visuais
- ✅ Animações suaves
- ✅ Modo escuro (suporte)

## 🔌 API Endpoints

### Autenticação
```
POST /usuarios/api/check-username/     # Verificar disponibilidade de username
POST /usuarios/api/check-email/        # Verificar disponibilidade de email
```

### Produtos
```
GET  /api/search-suggestions/          # Sugestões de busca
GET  /produtos/                        # Listar produtos
GET  /produto/<slug>/                  # Detalhes do produto
GET  /categoria/<slug>/                # Produtos por categoria
```

### Carrinho
```
GET    /carrinho/                      # Ver carrinho
POST   /carrinho/add/                  # Adicionar item
PUT    /carrinho/update/               # Atualizar item
DELETE /carrinho/remove/               # Remover item
GET    /carrinho/count/                # Contador de itens
```

### Pedidos
```
GET  /pedidos/                         # Listar pedidos
POST /pedidos/create/                  # Criar pedido
GET  /pedidos/<uuid>/                  # Detalhes do pedido
POST /pedidos/<uuid>/cancel/           # Cancelar pedido
```

## 👨‍💼 Administração

### Dashboard do Superadministrador

O sistema inclui um dashboard completo para superadministradores com:

- **Gestão de Usuários**: Ativar/desativar usuários
- **Upload de Imagens**: Sistema de upload para produtos
- **Gestão de Categorias**: CRUD completo de categorias
- **Relatórios**: Estatísticas e relatórios do sistema
- **Configurações**: Configurações globais do sistema

### Middleware de Segurança

O sistema inclui middleware personalizado (`AdminSecurityMiddleware`) que:

- Controla acesso às áreas administrativas
- Valida permissões de superadministrador
- Registra tentativas de acesso não autorizado
- Implementa rate limiting para segurança

## 🎨 Magic UI Integration

O projeto utiliza Magic UI para uma interface moderna e interativa:

### Componentes Implementados
- **Navbar Responsiva**: Com dropdown animado
- **Botões Interativos**: Com efeitos hover e ripple
- **Cards de Produto**: Design elegante e responsivo
- **Formulários**: Estilização consistente
- **Modais**: Para confirmações e detalhes
- **Loading States**: Indicadores de carregamento

### Correções e Melhorias
- **Cores Otimizadas**: Correção de contraste e legibilidade
- **Estados Ativos**: Indicadores visuais para navegação
- **Responsividade**: Adaptação para todos os dispositivos
- **Acessibilidade**: Suporte a leitores de tela

## 🔒 Segurança

### Medidas Implementadas
- **CSRF Protection**: Proteção contra ataques CSRF
- **SQL Injection**: Proteção via ORM Django
- **XSS Protection**: Sanitização de inputs
- **Secure Headers**: Headers de segurança configurados
- **Password Hashing**: BCrypt para senhas
- **Session Security**: Configurações seguras de sessão

### Configurações de Produção
```python
# settings.py
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
```

## 📱 Responsividade

O sistema é totalmente responsivo com breakpoints:

- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

### Recursos Mobile
- Menu hambúrguer
- Touch-friendly buttons
- Swipe gestures
- Otimização de imagens

## 🚀 Deploy

### Heroku
```bash
# Instalar Heroku CLI
heroku create seu-app-name
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=sua-chave-secreta
git push heroku main
heroku run python manage.py migrate
```

### Docker
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml .
RUN pip install uv && uv sync
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## 🧪 Testes

```bash
# Executar todos os testes
python manage.py test

# Testes específicos
python manage.py test usuarios
python manage.py test produtos

# Coverage
coverage run manage.py test
coverage report
```

## 📊 Performance

### Otimizações Implementadas
- **Database Indexing**: Índices otimizados
- **Query Optimization**: Select_related e prefetch_related
- **Image Compression**: Redimensionamento automático
- **Static Files**: Compressão e cache
- **Lazy Loading**: Carregamento sob demanda

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Padrões de Código
- Siga PEP 8 para Python
- Use docstrings em todas as funções
- Mantenha os commits pequenos e descritivos
- Adicione testes para novas funcionalidades

## 📝 Changelog

### v0.1.0 (2024-01-20)
- ✅ Sistema básico de e-commerce
- ✅ Integração Magic UI
- ✅ Sistema de autenticação
- ✅ Gestão de produtos e categorias
- ✅ Carrinho de compras
- ✅ Sistema de pedidos
- ✅ Integração PayPal
- ✅ Dashboard administrativo

## 🐛 Issues Conhecidos

- [ ] Otimização de queries em listas grandes
- [ ] Implementação de cache Redis
- [ ] Testes automatizados completos
- [ ] Documentação da API

## 📞 Suporte

Para suporte e dúvidas:

- 📧 Email: suporte@webcommerce.com
- 💬 Discord: [Link do servidor]
- 📖 Wiki: [Link da documentação]
- 🐛 Issues: [Link do GitHub Issues]

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

<div align="center">
  <p>Desenvolvido com ❤️ usando Django e Magic UI</p>
  <p>© 2024 Web Commerce. Todos os direitos reservados.</p>
</div>