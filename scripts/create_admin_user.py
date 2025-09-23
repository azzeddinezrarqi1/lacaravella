#!/usr/bin/env python
"""
Script pour créer un utilisateur administrateur
"""
import os
import sys
import django
from django.contrib.auth.models import User

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'caravela.settings')
django.setup()

def create_admin_user():
    """Créer un utilisateur administrateur"""
    
    username = 'admin'
    email = 'admin@lacaravela.com'
    password = 'admin123'
    
    # Vérifier si l'utilisateur existe déjà
    if User.objects.filter(username=username).exists():
        print(f"ℹ️  L'utilisateur '{username}' existe déjà")
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        print(f"✅ Mot de passe mis à jour pour '{username}'")
    else:
        # Créer le superutilisateur
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"✅ Superutilisateur '{username}' créé avec succès")
    
    print(f"📧 Email: {email}")
    print(f"🔑 Mot de passe: {password}")
    print(f"🌐 Interface d'administration: http://127.0.0.1:8000/admin/")
    print("\n📋 Permissions disponibles:")
    print("   ✅ Gestion des catégories (créer, modifier, supprimer)")
    print("   ✅ Gestion des produits (créer, modifier, supprimer)")
    print("   ✅ Gestion des utilisateurs")
    print("   ✅ Gestion des commandes")
    print("   ✅ Accès complet à l'administration Django")

if __name__ == '__main__':
    print("🚀 Création de l'utilisateur administrateur...")
    create_admin_user()
    print("✨ Terminé !")

