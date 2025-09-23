from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.

@login_required
def profile_view(request):
    """Vue du profil utilisateur"""
    return render(request, 'users/profile.html')

@login_required
def orders_view(request):
    """Vue des commandes de l'utilisateur"""
    return render(request, 'users/orders.html')

@login_required
def wishlist_view(request):
    """Vue de la liste de souhaits"""
    return render(request, 'users/wishlist.html')

@login_required
def add_to_wishlist(request, product_id):
    """Ajouter un produit à la liste de souhaits"""
    return JsonResponse({'success': True})

@login_required
def remove_from_wishlist(request, product_id):
    """Retirer un produit de la liste de souhaits"""
    return JsonResponse({'success': True})
