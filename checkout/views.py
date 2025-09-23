from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

def cart_view(request):
    """Vue du panier"""
    # Simulation d'un panier pour l'instant
    # Dans une vraie implémentation, vous récupéreriez le panier de l'utilisateur
    cart_items = []
    cart = {
        'subtotal': 0,
        'shipping_cost': 0,
        'discount_amount': 0,
        'total': 0,
        'total_items': 0
    }
    
    context = {
        'cart_items': cart_items,
        'cart': cart
    }
    
    return render(request, 'checkout/cart.html', context)

@require_POST
def add_to_cart(request):
    """Ajouter un produit au panier"""
    return JsonResponse({'success': True})

def remove_from_cart(request, item_id):
    """Retirer un article du panier"""
    return redirect('checkout:cart')

def update_cart_item(request, item_id):
    """Mettre à jour la quantité d'un article"""
    return JsonResponse({'success': True})

@login_required
def checkout_view(request):
    """Vue du checkout"""
    return render(request, 'checkout/checkout.html')

@login_required
def payment_view(request):
    """Vue du paiement"""
    return render(request, 'checkout/payment.html')

@csrf_exempt
def stripe_webhook(request):
    """Webhook Stripe"""
    return JsonResponse({'status': 'success'})

def order_confirmation(request, order_number):
    """Confirmation de commande"""
    return render(request, 'checkout/order_confirmation.html')
