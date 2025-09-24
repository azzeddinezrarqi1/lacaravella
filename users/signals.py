from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.contrib import messages


@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    """Handler pour ajouter un message de déconnexion réussie"""
    if user and request:
        messages.success(request, "Vous avez été déconnecté avec succès. À bientôt !")
