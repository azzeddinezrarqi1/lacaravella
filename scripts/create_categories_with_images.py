#!/usr/bin/env python
"""
Script pour créer des catégories d'exemple avec des images
"""
import os
import sys
import django
from django.core.files import File

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'caravela.settings')
django.setup()

from products.models import Category

def create_categories():
    """Créer des catégories avec leurs images"""
    
    categories_data = [
        {
            'name': 'Glaces Artisanales',
            'slug': 'glaces-artisanales',
            'description': 'Nos glaces artisanales préparées avec des ingrédients naturels et des recettes traditionnelles. Une texture onctueuse et des saveurs authentiques.',
            'image_path': 'static/images/categories/glaces-artisanales.svg',
            'order': 1
        },
        {
            'name': 'Sorbets',
            'slug': 'sorbets',
            'description': 'Des sorbets rafraîchissants à base de fruits frais, sans produits laitiers. Parfaits pour les chaudes journées d\'été.',
            'image_path': 'static/images/categories/sorbets.svg',
            'order': 2
        },
        {
            'name': 'Yaourts Glacés',
            'slug': 'yaourts-glaces',
            'description': 'Nos yaourts glacés crémeux et légers, parfaits pour une pause gourmande et équilibrée.',
            'image_path': 'static/images/categories/yaourts-glaces.svg',
            'order': 3
        },
        {
            'name': 'Gelato Italien',
            'slug': 'gelato-italien',
            'description': 'Authentique gelato italien avec une densité et une richesse incomparables. Préparé selon les traditions italiennes.',
            'image_path': 'static/images/categories/gelato.svg',
            'order': 4
        },
        {
            'name': 'Glaces Végétales',
            'slug': 'glaces-vegetales',
            'description': 'Nos glaces 100% végétales, sans lactose ni œufs. Des alternatives délicieuses pour tous les régimes alimentaires.',
            'image_path': 'static/images/categories/glaces-veganes.svg',
            'order': 5
        }
    ]
    
    for cat_data in categories_data:
        # Vérifier si la catégorie existe déjà
        category, created = Category.objects.get_or_create(
            slug=cat_data['slug'],
            defaults={
                'name': cat_data['name'],
                'description': cat_data['description'],
                'order': cat_data['order'],
                'is_active': True
            }
        )
        
        if created:
            print(f"✅ Catégorie '{cat_data['name']}' créée")
        else:
            print(f"ℹ️  Catégorie '{cat_data['name']}' existe déjà")
        
        # Ajouter l'image si elle n'existe pas déjà
        if not category.image and os.path.exists(cat_data['image_path']):
            try:
                with open(cat_data['image_path'], 'rb') as f:
                    category.image.save(
                        os.path.basename(cat_data['image_path']),
                        File(f),
                        save=True
                    )
                print(f"🖼️  Image ajoutée pour '{cat_data['name']}'")
            except Exception as e:
                print(f"❌ Erreur lors de l'ajout de l'image pour '{cat_data['name']}': {e}")
        elif category.image:
            print(f"ℹ️  Image déjà présente pour '{cat_data['name']}'")
        else:
            print(f"⚠️  Image non trouvée pour '{cat_data['name']}': {cat_data['image_path']}")

if __name__ == '__main__':
    print("🚀 Création des catégories avec images...")
    create_categories()
    print("✨ Terminé !")

