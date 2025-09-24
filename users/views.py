from django.shortcuts import render
from django.contrib.auth.decorators import login_required


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