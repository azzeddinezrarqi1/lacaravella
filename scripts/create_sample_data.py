#!/usr/bin/env python
"""
Script pour créer des données d'exemple pour La Caravela
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'caravela.settings')
django.setup()

from django.contrib.auth.models import User
from products.models import Category, Product
from django.core.files.base import ContentFile
from PIL import Image
import io

def create_sample_data():
    print("🍦 Création des données d'exemple pour La Caravela...")
    
    # Créer des catégories
    categories_data = [
        {'name': 'Glaces Classiques', 'description': 'Nos glaces traditionnelles aux parfums intemporels'},
        {'name': 'Glaces Exotiques', 'description': 'Des parfums du monde entier pour voyager'},
        {'name': 'Glaces Bio', 'description': 'Glaces biologiques aux ingrédients naturels'},
        {'name': 'Glaces Sans Lactose', 'description': 'Pour ceux qui préfèrent sans lactose'},
        {'name': 'Glaces Végétales', 'description': 'À base de lait d\'amande, coco ou soja'},
    ]
    
    categories = []
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        categories.append(category)
        if created:
            print(f"✅ Catégorie créée: {category.name}")
    
    # Créer des produits
    products_data = [
        {
            'name': 'Vanille de Madagascar',
            'description': 'Une glace onctueuse à la vanille bourbon de Madagascar',
            'price': 4.50,
            'category': categories[0],
            'is_featured': True,
            'stock_quantity': 100
        },
        {
            'name': 'Chocolat Noir 70%',
            'description': 'Glace intense au chocolat noir équitable',
            'price': 5.00,
            'category': categories[0],
            'is_featured': True,
            'stock_quantity': 80
        },
        {
            'name': 'Fraise Gariguette',
            'description': 'Glace aux fraises de Carpentras',
            'price': 4.80,
            'category': categories[0],
            'stock_quantity': 60
        },
        {
            'name': 'Mangue Passion',
            'description': 'Mélange exotique de mangue et fruit de la passion',
            'price': 5.50,
            'category': categories[1],
            'is_featured': True,
            'stock_quantity': 40
        },
        {
            'name': 'Coco Lime',
            'description': 'Glace coco rafraîchissante au zeste de citron vert',
            'price': 5.20,
            'category': categories[1],
            'stock_quantity': 50
        },
        {
            'name': 'Matcha Authentique',
            'description': 'Glace au thé vert matcha du Japon',
            'price': 6.00,
            'category': categories[1],
            'stock_quantity': 30
        },
        {
            'name': 'Lavande de Provence',
            'description': 'Glace parfumée à la lavande de Provence',
            'price': 5.80,
            'category': categories[2],
            'is_featured': True,
            'stock_quantity': 35
        },
        {
            'name': 'Miel de Lavande',
            'description': 'Glace au miel de lavande bio',
            'price': 5.30,
            'category': categories[2],
            'stock_quantity': 45
        },
        {
            'name': 'Amande Bio',
            'description': 'Glace à l\'amande sans lactose',
            'price': 5.60,
            'category': categories[3],
            'stock_quantity': 55
        },
        {
            'name': 'Coco Végétale',
            'description': 'Glace à base de lait de coco',
            'price': 5.40,
            'category': categories[4],
            'stock_quantity': 65
        },
        {
            'name': 'Soja Vanille',
            'description': 'Glace au lait de soja et vanille',
            'price': 5.10,
            'category': categories[4],
            'stock_quantity': 70
        },
        {
            'name': 'Pistache de Sicile',
            'description': 'Glace à la pistache AOP de Sicile',
            'price': 6.50,
            'category': categories[0],
            'is_featured': True,
            'stock_quantity': 25
        }
    ]
    
    for prod_data in products_data:
        product, created = Product.objects.get_or_create(
            name=prod_data['name'],
            defaults={
                'description': prod_data['description'],
                'price': prod_data['price'],
                'category': prod_data['category'],
                'is_featured': prod_data.get('is_featured', False),
                'stock_quantity': prod_data.get('stock_quantity', 50),
                'is_available': True
            }
        )
        if created:
            print(f"✅ Produit créé: {product.name} - {product.price}€")
    
    print("\n🎉 Données d'exemple créées avec succès !")
    print(f"📊 {len(categories)} catégories créées")
    print(f"🍦 {len(products_data)} produits créés")
    print("\n🌐 Vous pouvez maintenant visiter:")
    print("   - http://127.0.0.1:8000/ (Page d'accueil)")
    print("   - http://127.0.0.1:8000/demo/ (Démonstration des effets)")
    print("   - http://127.0.0.1:8000/admin/ (Administration Django)")
    print("   - http://127.0.0.1:8000/products/ (Liste des produits)")

if __name__ == '__main__':
    create_sample_data()






