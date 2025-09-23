import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import logging

# Configuration Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

logger = logging.getLogger(__name__)


class StripePaymentHandler:
    """Gestionnaire de paiements Stripe pour La Caravela"""
    
    def __init__(self):
        self.publishable_key = settings.STRIPE_PUBLISHABLE_KEY
        self.secret_key = settings.STRIPE_SECRET_KEY
        self.webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    
    def create_payment_intent(self, amount, currency='eur', metadata=None):
        """
        Créer un Payment Intent Stripe
        
        Args:
            amount (int): Montant en centimes
            currency (str): Devise (eur par défaut)
            metadata (dict): Métadonnées pour la commande
        
        Returns:
            dict: Payment Intent créé
        """
        try:
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                metadata=metadata or {},
                automatic_payment_methods={
                    'enabled': True,
                },
                # Configuration spécifique pour les glaces
                description="Commande La Caravela",
                receipt_email=metadata.get('customer_email') if metadata else None,
            )
            
            logger.info(f"Payment Intent créé: {intent.id}")
            return {
                'success': True,
                'client_secret': intent.client_secret,
                'payment_intent_id': intent.id,
                'amount': intent.amount,
                'currency': intent.currency,
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Erreur Stripe lors de la création du Payment Intent: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'error_type': type(e).__name__,
            }
    
    def confirm_payment(self, payment_intent_id):
        """
        Confirmer un paiement
        
        Args:
            payment_intent_id (str): ID du Payment Intent
        
        Returns:
            dict: Statut de la confirmation
        """
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            if intent.status == 'succeeded':
                return {
                    'success': True,
                    'status': intent.status,
                    'amount': intent.amount,
                    'currency': intent.currency,
                }
            else:
                return {
                    'success': False,
                    'status': intent.status,
                    'error': f"Paiement non confirmé: {intent.status}",
                }
                
        except stripe.error.StripeError as e:
            logger.error(f"Erreur Stripe lors de la confirmation: {str(e)}")
            return {
                'success': False,
                'error': str(e),
            }
    
    def create_refund(self, payment_intent_id, amount=None, reason='requested_by_customer'):
        """
        Créer un remboursement
        
        Args:
            payment_intent_id (str): ID du Payment Intent
            amount (int): Montant à rembourser en centimes (None pour remboursement total)
            reason (str): Raison du remboursement
        
        Returns:
            dict: Statut du remboursement
        """
        try:
            refund_params = {
                'payment_intent': payment_intent_id,
                'reason': reason,
            }
            
            if amount:
                refund_params['amount'] = amount
            
            refund = stripe.Refund.create(**refund_params)
            
            logger.info(f"Remboursement créé: {refund.id}")
            return {
                'success': True,
                'refund_id': refund.id,
                'amount': refund.amount,
                'status': refund.status,
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Erreur Stripe lors du remboursement: {str(e)}")
            return {
                'success': False,
                'error': str(e),
            }
    
    def get_payment_methods(self):
        """
        Obtenir les méthodes de paiement disponibles
        
        Returns:
            dict: Méthodes de paiement configurées
        """
        try:
            # Récupérer les méthodes de paiement configurées
            payment_methods = stripe.PaymentMethod.list(
                customer=None,  # Pour les méthodes globales
                type='card',
                limit=10
            )
            
            return {
                'success': True,
                'payment_methods': [
                    {
                        'id': pm.id,
                        'type': pm.type,
                        'card': {
                            'brand': pm.card.brand,
                            'last4': pm.card.last4,
                            'exp_month': pm.card.exp_month,
                            'exp_year': pm.card.exp_year,
                        } if pm.type == 'card' else None,
                    }
                    for pm in payment_methods.data
                ]
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Erreur Stripe lors de la récupération des méthodes de paiement: {str(e)}")
            return {
                'success': False,
                'error': str(e),
            }


# Configuration pour les webhooks Stripe
@csrf_exempt
@require_POST
def stripe_webhook(request):
    """
    Webhook Stripe pour traiter les événements de paiement
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        logger.error(f"Erreur de payload invalide: {str(e)}")
        return JsonResponse({'error': 'Payload invalide'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Erreur de signature: {str(e)}")
        return JsonResponse({'error': 'Signature invalide'}, status=400)
    
    # Traiter les événements
    if event['type'] == 'payment_intent.succeeded':
        handle_payment_succeeded(event)
    elif event['type'] == 'payment_intent.payment_failed':
        handle_payment_failed(event)
    elif event['type'] == 'charge.refunded':
        handle_refund_processed(event)
    
    return JsonResponse({'status': 'success'})


def handle_payment_succeeded(event):
    """Traiter un paiement réussi"""
    payment_intent = event['data']['object']
    order_id = payment_intent.metadata.get('order_id')
    
    if order_id:
        try:
            from .models import Order
            order = Order.objects.get(order_number=order_id)
            order.payment_status = 'paid'
            order.order_status = 'confirmed'
            order.save()
            
            logger.info(f"Commande {order_id} marquée comme payée")
            
            # Envoyer un email de confirmation
            send_order_confirmation_email(order)
            
        except Order.DoesNotExist:
            logger.error(f"Commande {order_id} non trouvée")
        except Exception as e:
            logger.error(f"Erreur lors du traitement de la commande {order_id}: {str(e)}")


def handle_payment_failed(event):
    """Traiter un échec de paiement"""
    payment_intent = event['data']['object']
    order_id = payment_intent.metadata.get('order_id')
    
    if order_id:
        try:
            from .models import Order
            order = Order.objects.get(order_number=order_id)
            order.payment_status = 'failed'
            order.save()
            
            logger.info(f"Commande {order_id} marquée comme échouée")
            
            # Envoyer un email d'échec
            send_payment_failed_email(order)
            
        except Order.DoesNotExist:
            logger.error(f"Commande {order_id} non trouvée")
        except Exception as e:
            logger.error(f"Erreur lors du traitement de l'échec {order_id}: {str(e)}")


def handle_refund_processed(event):
    """Traiter un remboursement"""
    charge = event['data']['object']
    order_id = charge.metadata.get('order_id')
    
    if order_id:
        try:
            from .models import Order
            order = Order.objects.get(order_number=order_id)
            order.payment_status = 'refunded'
            order.order_status = 'refunded'
            order.save()
            
            logger.info(f"Commande {order_id} marquée comme remboursée")
            
        except Order.DoesNotExist:
            logger.error(f"Commande {order_id} non trouvée")
        except Exception as e:
            logger.error(f"Erreur lors du traitement du remboursement {order_id}: {str(e)}")


def send_order_confirmation_email(order):
    """Envoyer un email de confirmation de commande"""
    try:
        from django.core.mail import send_mail
        from django.template.loader import render_to_string
        
        subject = f"Confirmation de commande - La Caravela #{order.order_number}"
        
        # Rendre le template d'email
        html_message = render_to_string('checkout/emails/order_confirmation.html', {
            'order': order,
        })
        
        send_mail(
            subject=subject,
            message='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.user.email],
            html_message=html_message,
        )
        
        logger.info(f"Email de confirmation envoyé pour la commande {order.order_number}")
        
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de l'email de confirmation: {str(e)}")


def send_payment_failed_email(order):
    """Envoyer un email d'échec de paiement"""
    try:
        from django.core.mail import send_mail
        from django.template.loader import render_to_string
        
        subject = f"Échec de paiement - La Caravela #{order.order_number}"
        
        html_message = render_to_string('checkout/emails/payment_failed.html', {
            'order': order,
        })
        
        send_mail(
            subject=subject,
            message='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.user.email],
            html_message=html_message,
        )
        
        logger.info(f"Email d'échec envoyé pour la commande {order.order_number}")
        
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de l'email d'échec: {str(e)}")


# Configuration pour les tests Stripe
def get_test_config():
    """Obtenir la configuration de test Stripe"""
    return {
        'publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
        'test_cards': {
            'success': '4242424242424242',
            'decline': '4000000000000002',
            'insufficient_funds': '4000000000009995',
            'expired': '4000000000000069',
            'incorrect_cvc': '4000000000000127',
        },
        'webhook_endpoint': '/checkout/stripe-webhook/',
    } 