from django.shortcuts import render
from django.http import HttpResponse
from products.models import Product, Category

def home_view(request):
    """Vue de la page d'accueil"""
    featured_products = Product.objects.filter(is_active=True).order_by('-is_featured', '-created_at')[:4]
    top_categories = Category.objects.filter(is_active=True).order_by('order', 'name')[:3]
    return render(request, 'home.html', {
        'title': 'La Caravela - Glaces Artisanales Premium',
        'message': 'Bienvenue chez La Caravela !',
        'featured_products': featured_products,
        'top_categories': top_categories,
    })

def about_view(request):
    """Vue de la page À propos"""
    return render(request, 'about.html', {
        'title': 'À propos - La Caravela'
    })

def contact_view(request):
    """Vue de la page Contact"""
    return render(request, 'contact.html', {
        'title': 'Contact - La Caravela'
    }) 