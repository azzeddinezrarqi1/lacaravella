from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Count
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
# from cacheops import cached_as, cached
from .models import Product, Category, Flavor, Allergen, CustomizationOption, ProductReview
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ProductForm
from .serializers import (
    ProductSerializer, CategorySerializer, FlavorSerializer,
    AllergenSerializer, CustomizationOptionSerializer, ProductReviewSerializer
)


# Vues classiques Django
@cache_page(60 * 15)  # Cache 15 minutes
def product_list(request):
    """Liste des produits"""
    products = Product.objects.filter(is_active=True).order_by('name')
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Données pour les filtres
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
    }
    
    return render(request, 'products/product_list.html', context)


@cache_page(60 * 15)  # Cache 15 minutes
def category_list(request):
    """Liste des catégories"""
    categories = Category.objects.filter(is_active=True).order_by('name')
    
    context = {
        'categories': categories,
    }
    
    return render(request, 'products/category_list.html', context)


@cache_page(60 * 30)  # Cache 30 minutes
def product_detail(request, slug):
    """Détail d'un produit"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    # Produits similaires
    similar_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]
    
    # Avis du produit
    reviews = product.reviews.filter(is_approved=True).order_by('-created_at')[:5]
    
    # Options de personnalisation
    customization_options = CustomizationOption.objects.filter(is_active=True).order_by('option_type', 'order')
    
    context = {
        'product': product,
        'similar_products': similar_products,
        'reviews': reviews,
        'customization_options': customization_options,
    }
    
    return render(request, 'products/product_detail.html', context)


@cache_page(60 * 60)  # Cache 1 heure
def category_detail(request, slug):
    """Détail d'une catégorie"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = category.products.filter(is_active=True)
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    
    return render(request, 'products/category_detail.html', context)


def search_products(request):
    """Recherche de produits"""
    query = request.GET.get('q', '')
    products = Product.objects.none()
    
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(flavors__name__icontains=query),
            is_active=True
        ).distinct()
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
    }
    
    return render(request, 'products/search_results.html', context)


def _is_staff(user):
    return user.is_staff or user.is_superuser


@login_required
@user_passes_test(_is_staff)
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect(product.get_absolute_url())
    else:
        form = ProductForm()
    return render(request, 'products/create.html', { 'form': form })


# API Views
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """API pour les produits"""
    queryset = Product.objects.filter(is_active=True).select_related('category')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'category__name']
    ordering_fields = ['name', 'base_price', 'created_at']
    ordering = ['name']

    # @cached_as(Product)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # @cached_as(Product)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @action(detail=True, methods=['get'])
    def flavors(self, request, pk=None):
        """Obtenir les parfums disponibles pour un produit"""
        product = self.get_object()
        flavors = product.flavors.filter(is_active=True)
        serializer = FlavorSerializer(flavors, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Obtenir les avis d'un produit"""
        product = self.get_object()
        reviews = product.reviews.filter(is_approved=True)
        serializer = ProductReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Obtenir les produits en vedette"""
        products = self.queryset.filter(is_featured=True)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def on_sale(self, request):
        """Obtenir les produits en promotion"""
        products = self.queryset.filter(sale_price__isnull=False)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """API pour les catégories"""
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # @cached_as(Category)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """Obtenir les produits d'une catégorie"""
        category = self.get_object()
        products = category.products.filter(is_active=True)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class FlavorViewSet(viewsets.ReadOnlyModelViewSet):
    """API pour les parfums"""
    queryset = Flavor.objects.filter(is_active=True)
    serializer_class = FlavorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CustomizationOptionViewSet(viewsets.ReadOnlyModelViewSet):
    """API pour les options de personnalisation"""
    queryset = CustomizationOption.objects.filter(is_active=True)
    serializer_class = CustomizationOptionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Obtenir les options par type"""
        option_type = request.GET.get('type')
        if option_type:
            options = self.queryset.filter(option_type=option_type)
        else:
            options = self.queryset
        serializer = self.get_serializer(options, many=True)
        return Response(serializer.data)


# Vues AJAX pour la personnalisation
def get_product_flavors(request, product_id):
    """Obtenir les parfums disponibles pour un produit"""
    product = get_object_or_404(Product, id=product_id)
    flavors = product.flavors.filter(is_active=True)
    
    data = []
    for flavor in flavors:
        try:
            product_flavor = product.productflavor_set.get(flavor=flavor)
            price_modifier = product_flavor.price_modifier
        except:
            price_modifier = 0
        
        data.append({
            'id': flavor.id,
            'name': flavor.name,
            'color': flavor.color,
            'price_modifier': float(price_modifier),
        })
    
    return JsonResponse({'flavors': data})


def get_customization_options(request):
    """Obtenir les options de personnalisation par type"""
    option_type = request.GET.get('type')
    options = CustomizationOption.objects.filter(is_active=True)
    
    if option_type:
        options = options.filter(option_type=option_type)
    
    data = []
    for option in options:
        data.append({
            'id': option.id,
            'name': option.name,
            'description': option.description,
            'price': float(option.price),
            'max_selections': option.max_selections,
            'image_url': option.image.url if option.image else None,
        })
    
    return JsonResponse({'options': data})


def calculate_customization_price(request):
    """Calculer le prix d'une personnalisation"""
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        
        base_price = float(data.get('base_price', 0))
        flavor_price_modifier = float(data.get('flavor_price_modifier', 0))
        customizations = data.get('customizations', [])
        
        # Calculer le prix des personnalisations
        customization_price = 0
        for customization in customizations:
            option_id = customization.get('option_id')
            quantity = customization.get('quantity', 1)
            
            try:
                option = CustomizationOption.objects.get(id=option_id)
                customization_price += float(option.price) * quantity
            except CustomizationOption.DoesNotExist:
                pass
        
        total_price = base_price + flavor_price_modifier + customization_price
        
        return JsonResponse({
            'base_price': base_price,
            'flavor_price_modifier': flavor_price_modifier,
            'customization_price': customization_price,
            'total_price': total_price,
        })
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
