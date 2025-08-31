from django.urls import path
from . import views
from .admin_views import (
    SuperAdminDashboardView,
    upload_image_view,
    manage_categories_view,
    system_users_view,
    toggle_user_status,
    system_reports_view
)

app_name = 'usuarios'

urlpatterns = [
    # URLs públicas
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('password-reset-confirm/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),
    
    # APIs
    path('api/check-username/', views.check_username_availability, name='check_username'),
    path('api/check-email/', views.check_email_availability, name='check_email'),
    
    # URLs do superadministrador
    path('superadmin/', SuperAdminDashboardView.as_view(), name='superadmin_dashboard'),
    path('superadmin/upload-image/', upload_image_view, name='upload_image'),
    path('superadmin/manage-categories/', manage_categories_view, name='manage_categories'),
    path('superadmin/system-users/', system_users_view, name='system_users'),
    path('superadmin/toggle-user/<int:user_id>/', toggle_user_status, name='toggle_user_status'),
    path('superadmin/reports/', system_reports_view, name='system_reports'),
]