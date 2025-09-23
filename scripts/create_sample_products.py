#!/usr/bin/env python
"""
Script pour créer des produits d'exemple dans les catégories
"""
import os
import sys
import django
from decimal import Decimal

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'caravela.settings')
django.setup()

from products.models import Category, Product, Flavor, Allergen

def create_sample_products():
    """Créer des produits d'exemple dans chaque catégorie"""
    
    # Récupérer les catégories
    categories = {
        'glaces-artisanales': Category.objects.get(slug='glaces-artisanales'),
        'sorbets': Category.objects.get(slug='sorbets'),
        'yaourts-glaces': Category.objects.get(slug='yaourts-glaces'),
        'gelato-italien': Category.objects.get(slug='gelato-italien'),
        'glaces-vegetales': Category.objects.get(slug='glaces-vegetales'),
    }
    
    products_data = [
        # Glaces Artisanales
        {
            'name': 'Vanille de Madagascar',
            'slug': 'vanille-madagascar',
            'description': 'Une glace à la vanille authentique avec de vrais gousses de vanille de Madagascar. Texture onctueuse et saveur intense.',
            'short_description': 'Glace vanille authentique',
            'category': categories['glaces-artisanales'],
            'product_type': 'ice_cream',
            'base_price': Decimal('25.00'),
            'is_featured': True
        },
        {
            'name': 'Chocolat Noir 70%',
            'slug': 'chocolat-noir-70',
            'description': 'Glace au chocolat noir intense avec 70% de cacao. Pour les amateurs de chocolat pur.',
            'short_description': 'Glace chocolat intense',
            'category': categories['glaces-artisanales'],
            'product_type': 'ice_cream',
            'base_price': Decimal('28.00'),
            'is_featured': True
        },
        
        # Sorbets
        {
            'name': 'Fraise Gariguette',
            'slug': 'fraise-gariguette',
            'description': 'Sorbet aux fraises Gariguette, fraîches et sucrées. Sans lactose, 100% fruits.',
            'short_description': 'Sorbet fraise naturel',
            'category': categories['sorbets'],
            'product_type': 'sorbet',
            'base_price': Decimal('22.00')
        },
        {
            'name': 'Citron Vert',
            'slug': 'citron-vert',
            'description': 'Sorbet citron vert rafraîchissant, parfait pour l\'été. Acidulé et désaltérant.',
            'short_description': 'Sorbet citron rafraîchissant',
            'category': categories['sorbets'],
            'product_type': 'sorbet',
            'base_price': Decimal('20.00')
        },
        
        # Yaourts Glacés
        {
            'name': 'Yaourt Nature',
            'slug': 'yaourt-nature',
            'description': 'Yaourt glacé nature, crémeux et léger. Parfait pour une pause gourmande.',
            'short_description': 'Yaourt glacé nature',
            'category': categories['yaourts-glaces'],
            'product_type': 'frozen_yogurt',
            'base_price': Decimal('18.00')
        },
        {
            'name': 'Yaourt aux Fruits Rouges',
            'slug': 'yaourt-fruits-rouges',
            'description': 'Yaourt glacé aux fruits rouges, équilibré entre douceur et acidité.',
            'short_description': 'Yaourt glacé fruits rouges',
            'category': categories['yaourts-glaces'],
            'product_type': 'frozen_yogurt',
            'base_price': Decimal('21.00')
        },
        
        # Gelato Italien
        {
            'name': 'Gelato Pistache',
            'slug': 'gelato-pistache',
            'description': 'Authentique gelato à la pistache de Sicile. Dense et crémeux comme en Italie.',
            'short_description': 'Gelato pistache sicilienne',
            'category': categories['gelato-italien'],
            'product_type': 'gelato',
            'base_price': Decimal('32.00'),
            'is_featured': True
        },
        {
            'name': 'Gelato Stracciatella',
            'slug': 'gelato-stracciatella',
            'description': 'Gelato vanille avec des éclats de chocolat noir. Un classique italien.',
            'short_description': 'Gelato stracciatella classique',
            'category': categories['gelato-italien'],
            'product_type': 'gelato',
            'base_price': Decimal('30.00')
        },
        
        # Glaces Végétales
        {
            'name': 'Coco-Lime',
            'slug': 'coco-lime',
            'description': 'Glace végétale coco-lime, sans lactose. Rafraîchissante et exotique.',
            'short_description': 'Glace végétale coco-lime',
            'category': categories['glaces-vegetales'],
            'product_type': 'ice_cream',
            'base_price': Decimal('24.00')
        },
        {
            'name': 'Amande Bio',
            'slug': 'amande-bio',
            'description': 'Glace végétale à l\'amande bio, onctueuse et naturelle. Sans gluten.',
            'short_description': 'Glace végétale amande bio',
            'category': categories['glaces-vegetales'],
            'product_type': 'ice_cream',
            'base_price': Decimal('26.00')
        }
    ]
    
    for product_data in products_data:
        # Vérifier si le produit existe déjà
        product, created = Product.objects.get_or_create(
            slug=product_data['slug'],
            defaults={
                'name': product_data['name'],
                'description': product_data['description'],
                'short_description': product_data['short_description'],
                'category': product_data['category'],
                'product_type': product_data['product_type'],
                'base_price': product_data['base_price'],
                'is_featured': product_data.get('is_featured', False),
                'is_active': True,
                'stock_quantity': 50,
                'is_customizable': True
            }
        )
        
        if created:
            print(f"✅ Produit '{product_data['name']}' créé dans {product_data['category'].name}")
        else:
            print(f"ℹ️  Produit '{product_data['name']}' existe déjà")

if __name__ == '__main__':
    print("🚀 Création des produits d'exemple...")
    create_sample_products()
    print("✨ Terminé !")
