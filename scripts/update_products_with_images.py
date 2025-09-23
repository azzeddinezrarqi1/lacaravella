#!/usr/bin/env python
"""
Script pour associer des images aux produits existants
"""
import os
import sys
import django
from django.core.files import File

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'caravela.settings')
django.setup()

from products.models import Product

def update_products_with_images():
    """Associer des images aux produits existants"""
    
    # Mapping des produits avec leurs images
    product_images = {
        'vanille-madagascar': 'static/images/products/vanille-madagascar.svg',
        'chocolat-noir-70': 'static/images/products/chocolat-noir.svg',
        'fraise-gariguette': 'static/images/products/fraise-gariguette.svg',
        'coco-lime': 'static/images/products/coco-lime.svg',
        'amande-bio': 'static/images/products/amande-bio.svg',
        'gelato-pistache': 'static/images/products/gelato-pistache.svg',
    }
    
    for slug, image_path in product_images.items():
        try:
            product = Product.objects.get(slug=slug)
            
            # Vérifier si le produit a déjà une image
            if product.image:
                print(f"ℹ️  Produit '{product.name}' a déjà une image")
                continue
            
            # Ajouter l'image si elle existe
            if os.path.exists(image_path):
                with open(image_path, 'rb') as f:
                    product.image.save(
                        os.path.basename(image_path),
                        File(f),
                        save=True
                    )
                print(f"🖼️  Image ajoutée pour '{product.name}'")
            else:
                print(f"⚠️  Image non trouvée pour '{product.name}': {image_path}")
                
        except Product.DoesNotExist:
            print(f"❌ Produit avec le slug '{slug}' non trouvé")
        except Exception as e:
            print(f"❌ Erreur lors de l'ajout de l'image pour '{slug}': {e}")

if __name__ == '__main__':
    print("🚀 Association des images aux produits...")
    update_products_with_images()
    print("✨ Terminé !")
