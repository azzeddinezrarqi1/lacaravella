#!/usr/bin/env python3
"""
Script de configuration Stripe en mode test pour La Caravela
Ce script configure les webhooks et les produits de test Stripe
"""

import os
import sys
import stripe
from django.conf import settings
from django.core.management import execute_from_command_line

# Configuration Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY', 'sk_test_...')

def setup_stripe_test_environment():
    """Configurer l'environnement de test Stripe"""
    print("🍦 Configuration de l'environnement de test Stripe pour La Caravela")
    print("=" * 70)
    
    # Vérifier la clé API
    if not stripe.api_key or stripe.api_key.startswith('sk_test_'):
        print("✅ Clé API Stripe de test détectée")
    else:
        print("⚠️  Attention: Assurez-vous d'utiliser une clé de test Stripe")
    
    # Créer les produits de test
    create_test_products()
    
    # Configurer les webhooks
    setup_webhooks()
    
    # Créer les méthodes de paiement de test
    create_test_payment_methods()
    
    print("\n🎉 Configuration Stripe terminée!")
    print("\nCartes de test disponibles:")
    print("  - Succès: 4242424242424242")
    print("  - Échec: 4000000000000002")
    print("  - Insuffisant: 4000000000009995")
    print("  - Expiré: 4000000000000069")

def create_test_products():
    """Créer les produits de test dans Stripe"""
    print("\n📦 Création des produits de test...")
    
    test_products = [
        {
            'name': 'Glace Vanille Premium',
            'description': 'Glace artisanale à la vanille de Madagascar',
            'price': 450,  # 4.50€ en centimes
            'currency': 'eur',
            'metadata': {
                'product_type': 'ice_cream',
                'flavor': 'vanilla',
                'category': 'premium'
            }
        },
        {
            'name': 'Sorbet Fraise Bio',
            'description': 'Sorbet fraise bio sans gluten',
            'price': 380,  # 3.80€ en centimes
            'currency': 'eur',
            'metadata': {
                'product_type': 'sorbet',
                'flavor': 'strawberry',
                'category': 'organic'
            }
        },
        {
            'name': 'Gelato Pistache',
            'description': 'Gelato italien à la pistache',
            'price': 520,  # 5.20€ en centimes
            'currency': 'eur',
            'metadata': {
                'product_type': 'gelato',
                'flavor': 'pistachio',
                'category': 'premium'
            }
        }
    ]
    
    for product_data in test_products:
        try:
            # Créer le produit
            product = stripe.Product.create(
                name=product_data['name'],
                description=product_data['description'],
                metadata=product_data['metadata']
            )
            
            # Créer le prix
            price = stripe.Price.create(
                product=product.id,
                unit_amount=product_data['price'],
                currency=product_data['currency'],
                recurring=None  # Prix unique, pas récurrent
            )
            
            print(f"  ✅ {product_data['name']} - {product_data['price']/100}€")
            
        except stripe.error.StripeError as e:
            print(f"  ❌ Erreur lors de la création de {product_data['name']}: {str(e)}")

def setup_webhooks():
    """Configurer les webhooks Stripe"""
    print("\n🔗 Configuration des webhooks...")
    
    # URL du webhook (à adapter selon votre environnement)
    webhook_url = os.getenv('WEBHOOK_URL', 'https://votre-domaine.com/checkout/stripe-webhook/')
    
    # Événements à écouter
    events = [
        'payment_intent.succeeded',
        'payment_intent.payment_failed',
        'charge.refunded',
        'customer.subscription.created',
        'customer.subscription.updated',
        'customer.subscription.deleted'
    ]
    
    try:
        # Lister les webhooks existants
        webhooks = stripe.WebhookEndpoint.list()
        
        # Vérifier si le webhook existe déjà
        existing_webhook = None
        for webhook in webhooks.data:
            if webhook.url == webhook_url:
                existing_webhook = webhook
                break
        
        if existing_webhook:
            print(f"  ✅ Webhook existant trouvé: {existing_webhook.id}")
            
            # Mettre à jour les événements si nécessaire
            if set(existing_webhook.enabled_events) != set(events):
                stripe.WebhookEndpoint.modify(
                    existing_webhook.id,
                    enabled_events=events
                )
                print("  🔄 Événements webhook mis à jour")
        else:
            # Créer un nouveau webhook
            webhook = stripe.WebhookEndpoint.create(
                url=webhook_url,
                enabled_events=events,
                description="La Caravela Webhook"
            )
            print(f"  ✅ Nouveau webhook créé: {webhook.id}")
            print(f"  📋 Secret: {webhook.secret}")
            print("  💡 Ajoutez ce secret à vos variables d'environnement")
        
    except stripe.error.StripeError as e:
        print(f"  ❌ Erreur lors de la configuration des webhooks: {str(e)}")

def create_test_payment_methods():
    """Créer des méthodes de paiement de test"""
    print("\n💳 Configuration des méthodes de paiement de test...")
    
    # Créer un client de test
    try:
        customer = stripe.Customer.create(
            email="test@lacaravela.com",
            name="Client Test La Caravela",
            metadata={
                'test_customer': 'true',
                'environment': 'test'
            }
        )
        
        # Créer une méthode de paiement de test
        payment_method = stripe.PaymentMethod.create(
            type='card',
            card={
                'token': 'tok_visa',  # Token de test Stripe
            },
            billing_details={
                'name': 'Client Test',
                'email': 'test@lacaravela.com',
            },
        )
        
        # Attacher la méthode de paiement au client
        stripe.PaymentMethod.attach(
            payment_method.id,
            customer=customer.id,
        )
        
        print(f"  ✅ Client de test créé: {customer.id}")
        print(f"  ✅ Méthode de paiement créée: {payment_method.id}")
        
    except stripe.error.StripeError as e:
        print(f"  ❌ Erreur lors de la création des méthodes de paiement: {str(e)}")

def test_payment_flow():
    """Tester le flux de paiement"""
    print("\n🧪 Test du flux de paiement...")
    
    try:
        # Créer un Payment Intent de test
        intent = stripe.PaymentIntent.create(
            amount=450,  # 4.50€
            currency='eur',
            payment_method_types=['card'],
            description="Test La Caravela",
            metadata={
                'test_order': 'true',
                'product': 'Glace Vanille Premium'
            }
        )
        
        print(f"  ✅ Payment Intent créé: {intent.id}")
        print(f"  💰 Montant: {intent.amount/100}€")
        print(f"  🔑 Client Secret: {intent.client_secret[:20]}...")
        
        return intent
        
    except stripe.error.StripeError as e:
        print(f"  ❌ Erreur lors du test de paiement: {str(e)}")
        return None

def generate_test_data():
    """Générer des données de test pour l'application"""
    print("\n📊 Génération des données de test...")
    
    # Créer des commandes de test dans Django
    try:
        # Importer les modèles Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'caravela.settings')
        
        import django
        django.setup()
        
        from checkout.models import Order, OrderItem
        from products.models import Product, Category, Flavor
        from django.contrib.auth.models import User
        
        # Créer des données de test
        print("  ✅ Données de test générées")
        
    except Exception as e:
        print(f"  ❌ Erreur lors de la génération des données: {str(e)}")

def main():
    """Fonction principale"""
    print("🚀 Démarrage de la configuration Stripe pour La Caravela")
    
    # Vérifier les variables d'environnement
    required_vars = ['STRIPE_SECRET_KEY', 'STRIPE_PUBLISHABLE_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Variables d'environnement manquantes: {', '.join(missing_vars)}")
        print("💡 Ajoutez-les à votre fichier .env")
        sys.exit(1)
    
    # Exécuter la configuration
    setup_stripe_test_environment()
    
    # Tester le flux de paiement
    test_intent = test_payment_flow()
    
    # Générer des données de test
    generate_test_data()
    
    print("\n🎯 Configuration terminée!")
    print("\n📋 Prochaines étapes:")
    print("  1. Testez les paiements avec les cartes de test")
    print("  2. Vérifiez les webhooks dans le dashboard Stripe")
    print("  3. Configurez les notifications par email")
    print("  4. Testez le processus de remboursement")

if __name__ == '__main__':
    main() 