# 🛒 Web Commerce - Complete E-commerce System

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2.5-green.svg)
![Magic UI](https://img.shields.io/badge/Magic%20UI-Latest-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A modern and complete e-commerce system developed with Django, featuring an elegant interface with Magic UI and advanced administration functionalities.

## 📋 Table of Contents

- [Features](#-features)
- [Technologies Used](#-technologies-used)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Functionalities](#-functionalities)
- [API Endpoints](#-api-endpoints)
- [Administration](#-administration)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

- **Modern Interface**: Responsive design with Magic UI components
- **Complete Authentication System**: Login, registration, password recovery
- **Product Management**: Complete CRUD with categories and images
- **Shopping Cart**: Persistent cart system
- **Order System**: Complete order management with status tracking
- **PayPal Integration**: Secure payments via PayPal
- **Administrative Panel**: Complete dashboard for superadministrators
- **Multi-currency**: Support for USD, JPY, and BRL
- **Notification System**: Automatic emails and notifications
- **Advanced Security**: Custom security middleware

## 🚀 Technologies Used

### Backend
- **Django 5.2.5** - Main web framework
- **Django REST Framework 3.16.1** - REST API
- **SQLite** - Database (development)
- **PostgreSQL** - Database (production)
- **Pillow 11.3.0** - Image processing
- **PayPal REST SDK 1.13.3** - Payment integration

### Frontend
- **Magic UI** - UI component library
- **HTML5/CSS3** - Structure and styling
- **JavaScript** - Interactivity
- **Font Awesome** - Icons

### Tools
- **Python Decouple** - Configuration management
- **BCrypt** - Password encryption
- **UV** - Dependency manager

## 📁 Project Structure

```
web_commerce/
├── 📁 ecommerce_project/          # Main Django configurations
│   ├── settings.py                # Project settings
│   ├── urls.py                   # Main URLs
│   └── wsgi.py                   # WSGI configuration
├── 📁 core/                      # Main app (home, products)
│   ├── models.py                 # Main models
│   ├── views.py                  # Core views
│   └── urls.py                   # Core URLs
├── 📁 usuarios/                  # User system
│   ├── models.py                 # UserProfile, PasswordResetToken
│   ├── views.py                  # Authentication and profile
│   ├── admin_views.py            # Administrative views
│   └── permissions.py            # Security middleware
├── 📁 produtos/                  # Product management
│   ├── models.py                 # Product, Category, ProductImage
│   ├── views.py                  # Product CRUD
│   └── forms.py                  # Product forms
├── 📁 carrinho/                  # Cart system
│   ├── models.py                 # CartItem, Cart
│   └── views.py                  # Cart management
├── 📁 pedidos/                   # Order system
│   ├── models.py                 # Order, OrderItem
│   └── views.py                  # Order processing
├── 📁 static/                    # Static files
│   ├── 📁 css/                   # CSS styles
│   │   ├── magic-ui-fixes.css    # Magic UI fixes
│   │   ├── navbar-dropdown-fix.css # Navbar fixes
│   │   └── input-text-color-fix.css # Input fixes
│   └── 📁 js/                    # JavaScript scripts
│       ├── magic-ui-components.js # Magic UI components
│       └── navbar-active-states.js # Navbar active states
├── 📁 templates/                 # HTML templates
│   ├── base.html                 # Base template
│   ├── 📁 core/                  # Core templates
│   ├── 📁 usuarios/              # User templates
│   ├── 📁 carrinho/              # Cart templates
│   └── 📁 pedidos/               # Order templates
├── 📁 media/                     # Media files
├── db.sqlite3                    # SQLite database
├── pyproject.toml               # Project configuration
└── README.md                    # This file
```

## 🔧 Installation

### Prerequisites
- Python 3.12+
- UV (dependency manager)
- Git

### Step by step

1. **Clone the repository**
```bash
git clone https://github.com/your-username/web-commerce.git
cd web-commerce
```

2. **Install dependencies**
```bash
uv sync
```

3. **Activate virtual environment**
```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

4. **Configure environment variables**
```bash
cp .env.example .env
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Start the server**
```bash
python manage.py runserver
```

## ⚙️ Configuration

### Environment Variables (.env)

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# PayPal
PAYPAL_CLIENT_ID=your-paypal-client-id
PAYPAL_CLIENT_SECRET=your-paypal-client-secret
PAYPAL_MODE=sandbox  # or 'live' for production

# Email
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Security
USE_HTTPS=False
SECURE_COOKIES=False
```

### Production Settings

For production, adjust the following settings:

```env
DEBUG=False
USE_HTTPS=True
SECURE_COOKIES=True
PAYPAL_MODE=live
```

## 🎯 Usage

### System Access

- **Main Site**: http://localhost:8000/
- **Django Admin**: http://localhost:8000/admin/
- **Admin Dashboard**: http://localhost:8000/usuarios/superadmin/

### Default Credentials

**Superadministrator**:
- Email: admin@sistema.com
- Password: admin123

## 🔥 Functionalities

### 👤 User System
- ✅ User registration with validation
- ✅ Secure Login/Logout
- ✅ Password recovery via email
- ✅ Complete user profile
- ✅ Avatar upload
- ✅ Currency preferences
- ✅ Notification settings

### 🛍️ Product Management
- ✅ Complete product CRUD
- ✅ Category system
- ✅ Multiple image upload
- ✅ Stock control
- ✅ Multi-currency support
- ✅ Active/inactive products
- ✅ Advanced search and filters

### 🛒 Shopping Cart
- ✅ Add/remove products
- ✅ Update quantities
- ✅ Persistent cart
- ✅ Stock validation
- ✅ Automatic total calculation

### 📦 Order System
- ✅ Complete checkout
- ✅ Multiple order statuses
- ✅ PayPal integration
- ✅ Order history
- ✅ Delivery tracking
- ✅ Refund system

### 🔐 Administration
- ✅ Administrative dashboard
- ✅ User management
- ✅ System reports
- ✅ Image upload
- ✅ Category management
- ✅ Permission control

### 🎨 Interface
- ✅ Responsive design
- ✅ Magic UI components
- ✅ Interactive navbar
- ✅ Visual active states
- ✅ Smooth animations
- ✅ Dark mode (support)

## 🔌 API Endpoints

### Authentication
```
POST /usuarios/api/check-username/     # Check username availability
POST /usuarios/api/check-email/        # Check email availability
```

### Products
```
GET  /api/search-suggestions/          # Search suggestions
GET  /produtos/                        # List products
GET  /produto/<slug>/                  # Product details
GET  /categoria/<slug>/                # Products by category
```

### Cart
```
GET    /carrinho/                      # View cart
POST   /carrinho/add/                  # Add item
PUT    /carrinho/update/               # Update item
DELETE /carrinho/remove/               # Remove item
GET    /carrinho/count/                # Item counter
```

### Orders
```
GET  /pedidos/                         # List orders
POST /pedidos/create/                  # Create order
GET  /pedidos/<uuid>/                  # Order details
POST /pedidos/<uuid>/cancel/           # Cancel order
```

## 👨‍💼 Administration

### Superadministrator Dashboard

The system includes a complete dashboard for superadministrators with:

- **User Management**: Activate/deactivate users
- **Image Upload**: Upload system for products
- **Category Management**: Complete category CRUD
- **Reports**: System statistics and reports
- **Settings**: Global system settings

### Security Middleware

The system includes custom middleware (`AdminSecurityMiddleware`) that:

- Controls access to administrative areas
- Validates superadministrator permissions
- Logs unauthorized access attempts
- Implements rate limiting for security

## 🎨 Magic UI Integration

The project uses Magic UI for a modern and interactive interface:

### Implemented Components
- **Responsive Navbar**: With animated dropdown
- **Interactive Buttons**: With hover and ripple effects
- **Product Cards**: Elegant and responsive design
- **Forms**: Consistent styling
- **Modals**: For confirmations and details
- **Loading States**: Loading indicators

### Fixes and Improvements
- **Optimized Colors**: Contrast and readability fixes
- **Active States**: Visual indicators for navigation
- **Responsiveness**: Adaptation for all devices
- **Accessibility**: Screen reader support

## 🔒 Security

### Implemented Measures
- **CSRF Protection**: Protection against CSRF attacks
- **SQL Injection**: Protection via Django ORM
- **XSS Protection**: Input sanitization
- **Secure Headers**: Configured security headers
- **Password Hashing**: BCrypt for passwords
- **Session Security**: Secure session configurations

### Production Settings
```python
# settings.py
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
```

## 📱 Responsiveness

The system is fully responsive with breakpoints:

- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

### Mobile Features
- Hamburger menu
- Touch-friendly buttons
- Swipe gestures
- Image optimization

## 🚀 Deploy

### Heroku
```bash
# Install Heroku CLI
heroku create your-app-name
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key
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

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Specific tests
python manage.py test usuarios
python manage.py test produtos

# Coverage
coverage run manage.py test
coverage report
```

## 📊 Performance

### Implemented Optimizations
- **Database Indexing**: Optimized indexes
- **Query Optimization**: Select_related and prefetch_related
- **Image Compression**: Automatic resizing
- **Static Files**: Compression and cache
- **Lazy Loading**: On-demand loading

## 🤝 Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Standards
- Follow PEP 8 for Python
- Use docstrings in all functions
- Keep commits small and descriptive
- Add tests for new features

## 📝 Changelog

### v0.1.0 (2024-01-20)
- ✅ Basic e-commerce system
- ✅ Magic UI integration
- ✅ Authentication system
- ✅ Product and category management
- ✅ Shopping cart
- ✅ Order system
- ✅ PayPal integration
- ✅ Administrative dashboard

## 🐛 Known Issues

- [ ] Query optimization for large lists
- [ ] Redis cache implementation
- [ ] Complete automated tests
- [ ] API documentation

## 📞 Support

For support and questions:

- 📧 Email: support@webcommerce.com
- 💬 Discord: [Server link]
- 📖 Wiki: [Documentation link]
- 🐛 Issues: [GitHub Issues link]

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <p>Developed with ❤️ using Django and Magic UI</p>
  <p>© 2024 Web Commerce. All rights reserved.</p>
</div>