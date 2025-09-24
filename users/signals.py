from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)


@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    """Handler pour ajouter un message de déconnexion réussie"""
    try:
        if user and request:
            messages.success(request, "Vous avez été déconnecté avec succès. À bientôt !")
            logger.info(f"User {user.username} logged out successfully")
    except Exception as e:
        logger.error(f"Error in logout handler: {e}")
