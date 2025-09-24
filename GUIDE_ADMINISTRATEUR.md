# Guide de l'Administrateur - La Caravela

## 🔐 Accès à l'Interface d'Administration

**URL :** http://127.0.0.1:8000/admin/  
**Nom d'utilisateur :** `admin`  
**Mot de passe :** `admin123`

## 📋 Fonctionnalités Disponibles

### 🏷️ Gestion des Catégories

L'administrateur peut :

- ✅ **Créer** de nouvelles catégories
- ✅ **Modifier** les catégories existantes
- ✅ **Supprimer** des catégories
- ✅ **Uploader des images** pour les catégories
- ✅ **Gérer l'ordre d'affichage** des catégories
- ✅ **Activer/Désactiver** des catégories

**Champs disponibles :**
- Nom de la catégorie
- Slug (URL automatique)
- Description
- Image (upload)
- Ordre d'affichage
- Statut actif/inactif

### 🍦 Gestion des Produits

L'administrateur peut :

- ✅ **Créer** de nouveaux produits
- ✅ **Modifier** les produits existants
- ✅ **Supprimer** des produits
- ✅ **Uploader des images** pour les produits
- ✅ **Gérer les prix** (prix de base et prix en promotion)
- ✅ **Associer des catégories** aux produits
- ✅ **Gérer les allergènes** et parfums
- ✅ **Définir les produits en vedette**
- ✅ **Gérer le stock** et les quantités

**Champs disponibles :**
- Nom du produit
- Description (courte et complète)
- Image (upload)
- Catégorie
- Type de produit (glace, sorbet, yaourt glacé, gelato)
- Prix de base et prix en promotion
- Allergènes et parfums
- Stock et quantités
- Statut actif/inactif et en vedette

### 👥 Gestion des Utilisateurs

- ✅ **Créer** de nouveaux utilisateurs
- ✅ **Modifier** les profils utilisateurs
- ✅ **Gérer les permissions** des utilisateurs
- ✅ **Activer/Désactiver** des comptes

### 🛒 Gestion des Commandes

- ✅ **Voir** toutes les commandes
- ✅ **Modifier** le statut des commandes
- ✅ **Gérer** les détails des commandes

## 🎯 Guide d'Utilisation Rapide

### 1. Ajouter une Nouvelle Catégorie

1. Aller dans **Catégories** → **Ajouter**
2. Remplir les champs :
   - **Nom** : "Nouvelle Catégorie"
   - **Description** : Description de la catégorie
   - **Image** : Uploader une image
   - **Ordre** : Numéro pour l'ordre d'affichage
3. Cliquer sur **Enregistrer**

### 2. Ajouter un Nouveau Produit

1. Aller dans **Produits** → **Ajouter**
2. Remplir les champs :
   - **Nom** : "Nouveau Produit"
   - **Description** : Description complète
   - **Description courte** : Résumé
   - **Image** : Uploader une image
   - **Catégorie** : Sélectionner une catégorie
   - **Type de produit** : Choisir le type
   - **Prix de base** : Prix en MAD
   - **Stock** : Quantité disponible
3. Cliquer sur **Enregistrer**

### 3. Modifier une Catégorie Existante

1. Aller dans **Catégories** → Cliquer sur la catégorie
2. Modifier les champs souhaités
3. Cliquer sur **Enregistrer**

### 4. Supprimer un Élément

1. Aller dans la section souhaitée
2. Sélectionner l'élément à supprimer
3. Cliquer sur **Supprimer**
4. Confirmer la suppression

## 🖼️ Gestion des Images

### Formats Supportés
- **Images** : JPG, PNG, SVG, GIF
- **Taille recommandée** : 400x300 pixels minimum
- **Poids maximum** : 5MB par image

### Upload d'Images
1. Cliquer sur **Choisir un fichier**
2. Sélectionner l'image
3. L'image sera automatiquement redimensionnée si nécessaire

## ⚠️ Bonnes Pratiques

### Sécurité
- ✅ Changer le mot de passe par défaut
- ✅ Utiliser des mots de passe forts
- ✅ Se déconnecter après utilisation

### Gestion du Contenu
- ✅ Vérifier les images avant publication
- ✅ Tester les modifications sur le site
- ✅ Sauvegarder régulièrement les données

### Performance
- ✅ Optimiser les images avant upload
- ✅ Ne pas surcharger avec trop de produits
- ✅ Gérer l'ordre d'affichage des catégories

## 🆘 Support

En cas de problème :
1. Vérifier que le serveur Django est en cours d'exécution
2. Vérifier les permissions de l'utilisateur
3. Consulter les logs Django pour les erreurs

## 📞 Contact

Pour toute question technique, contacter l'équipe de développement.


