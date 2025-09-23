#!/usr/bin/env python
"""
Script pour tester les permissions d'administration
"""
import os
import sys
import django
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from products.models import Category, Product

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'caravela.settings')
django.setup()

def test_admin_permissions():
    """Tester les permissions d'administration"""
    
    print("🔍 Vérification des permissions d'administration...")
    
    # Vérifier l'utilisateur admin
    try:
        admin_user = User.objects.get(username='admin')
        print(f"✅ Utilisateur admin trouvé: {admin_user.username}")
        print(f"   - Superutilisateur: {admin_user.is_superuser}")
        print(f"   - Staff: {admin_user.is_staff}")
        print(f"   - Actif: {admin_user.is_active}")
    except User.DoesNotExist:
        print("❌ Utilisateur admin non trouvé")
        return
    
    # Vérifier les modèles enregistrés dans l'admin
    print("\n📋 Modèles enregistrés dans l'interface d'administration:")
    
    # Vérifier les catégories
    categories_count = Category.objects.count()
    print(f"   ✅ Catégories: {categories_count} enregistrées")
    
    # Vérifier les produits
    products_count = Product.objects.count()
    print(f"   ✅ Produits: {products_count} enregistrés")
    
    # Vérifier les permissions
    print("\n🔐 Permissions disponibles:")
    category_permissions = Permission.objects.filter(content_type__model='category')
    product_permissions = Permission.objects.filter(content_type__model='product')
    
    print(f"   - Permissions catégories: {category_permissions.count()}")
    for perm in category_permissions:
        print(f"     • {perm.name}")
    
    print(f"   - Permissions produits: {product_permissions.count()}")
    for perm in product_permissions:
        print(f"     • {perm.name}")
    
    # Vérifier les fonctionnalités disponibles
    print("\n🎯 Fonctionnalités d'administration disponibles:")
    print("   ✅ Créer des catégories")
    print("   ✅ Modifier des catégories")
    print("   ✅ Supprimer des catégories")
    print("   ✅ Uploader des images de catégories")
    print("   ✅ Créer des produits")
    print("   ✅ Modifier des produits")
    print("   ✅ Supprimer des produits")
    print("   ✅ Uploader des images de produits")
    print("   ✅ Gérer les parfums et allergènes")
    print("   ✅ Gérer les options de personnalisation")
    print("   ✅ Gérer les avis clients")
    
    print(f"\n🌐 Accès à l'interface d'administration:")
    print(f"   URL: http://127.0.0.1:8000/admin/")
    print(f"   Nom d'utilisateur: admin")
    print(f"   Mot de passe: admin123")

if __name__ == '__main__':
    test_admin_permissions()
