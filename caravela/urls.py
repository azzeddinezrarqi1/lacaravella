"""
URL configuration for caravela project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    # Admin Django
    path('admin/', admin.site.urls),
    
    # Applications principales
    path('', views.home_view, name='home'),
    path('test/', TemplateView.as_view(template_name='test.html'), name='test'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('demo/', TemplateView.as_view(template_name='demo.html'), name='demo'),
    path('', include('products.urls')),
    path('checkout/', include('checkout.urls')),
    path('users/', include('users.urls')),
    path('analytics/', include('analytics.urls')),
    
    # Authentification (Django Allauth)
    path('accounts/', include('allauth.urls')),
    
    # API REST (laisse le router sous /)
    path('legal/terms/', TemplateView.as_view(template_name='legal/terms.html'), name='legal_terms'),
    path('legal/privacy/', TemplateView.as_view(template_name='legal/privacy.html'), name='legal_privacy'),
    path('legal/shipping/', TemplateView.as_view(template_name='legal/shipping.html'), name='legal_shipping'),
    path('legal/returns/', TemplateView.as_view(template_name='legal/returns.html'), name='legal_returns'),
]

# URLs pour les fichiers média en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Django Debug Toolbar
    # import debug_toolbar
    # urlpatterns += [
    #     path('__debug__/', include(debug_toolbar.urls)),
    # ]

# Configuration du site admin
admin.site.site_header = "La Caravela - Administration"
admin.site.site_title = "La Caravela Admin"
admin.site.index_title = "Bienvenue dans l'administration de La Caravela"
