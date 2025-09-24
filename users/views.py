from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages


@login_required
def custom_logout_view(request):
    """Vue personnalisée de déconnexion avec message unique"""
    # Effectuer la déconnexion d'abord
    logout(request)
    
    # Effacer tous les messages existants (après logout)
    storage = messages.get_messages(request)
    list(storage)  # Consommer tous les messages
    
    # Ajouter seulement notre message personnalisé
    messages.success(request, "Vous avez été déconnecté avec succès. À bientôt !")
    
    # Rediriger vers la page de connexion
    return redirect('account_login')


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