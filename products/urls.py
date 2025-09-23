from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'products'

# Router pour l'API REST
router = DefaultRouter()
router.register(r'api/products', views.ProductViewSet, basename='api-product')
router.register(r'api/categories', views.CategoryViewSet, basename='api-category')
router.register(r'api/flavors', views.FlavorViewSet, basename='api-flavor')
router.register(r'api/customizations', views.CustomizationOptionViewSet, basename='api-customization')

# URLs classiques Django
urlpatterns = [
    # Pages principales (sous /products/)
    path('products/', views.product_list, name='product_list'),
    path('categories/', views.category_list, name='category_list'),
    path('products/search/', views.search_products, name='search_products'),
    path('products/category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('products/product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('products/add/', views.product_create, name='product_create'),
    
    # API AJAX pour la personnalisation
    path('ajax/product/<int:product_id>/flavors/', views.get_product_flavors, name='get_product_flavors'),
    path('ajax/customization-options/', views.get_customization_options, name='get_customization_options'),
    path('ajax/calculate-price/', views.calculate_customization_price, name='calculate_customization_price'),
    
    # Inclure les URLs de l'API REST
    path('', include(router.urls)),
] 