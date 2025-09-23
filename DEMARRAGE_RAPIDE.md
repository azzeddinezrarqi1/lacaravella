# 🚀 Guide de Démarrage Rapide - La Caravela

## ✅ Projet Fonctionnel !

Le projet La Caravela est maintenant **opérationnel** et prêt à être utilisé.

## 📋 Prérequis

- Python 3.11+
- pip (gestionnaire de packages Python)

## 🚀 Installation Rapide

### 1. Cloner le projet
```bash
git clone https://github.com/votre-username/lacaravella.git
cd lacaravella
```

### 2. Installer les dépendances
```bash
pip install -r requirements-dev.txt
```

### 3. Configurer l'environnement
```bash
# Copier le fichier d'exemple
cp env.example .env

# Éditer le fichier .env avec vos configurations
# (optionnel pour le développement)
```

### 4. Initialiser la base de données
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Lancer le serveur
```bash
python manage.py runserver
```

## 🌐 Accès à l'Application

- **Page d'accueil** : http://localhost:8000/
- **Admin Django** : http://localhost:8000/admin/
- **API REST** : http://localhost:8000/api/
- **Produits** : http://localhost:8000/products/

## 🔧 Configuration

### Variables d'Environnement (Optionnel)

Créer un fichier `.env` à la racine du projet :

```env
# Configuration de base
SECRET_KEY=votre-clé-secrète-django
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Stripe (optionnel pour les tests)
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
```

### Base de Données

Par défaut, le projet utilise **SQLite** pour le développement.
Pour la production, configurez PostgreSQL dans `settings.py`.

## 🎯 Fonctionnalités Disponibles

### ✅ Pages Statiques
- **Page d'accueil** avec design moderne
- **Page À propos** avec histoire de la marque
- **Page Contact** avec formulaire

### ✅ Administration
- **Interface d'administration** Django complète
- **Gestion des produits** et catégories
- **Gestion des utilisateurs** et commandes

### ✅ API REST
- **Endpoints produits** : `/api/products/`
- **Endpoints catégories** : `/api/categories/`
- **Endpoints parfums** : `/api/flavors/`

### ✅ Modèles de Données
- **Produits** avec personnalisation
- **Commandes** et panier
- **Utilisateurs** avec profils étendus
- **Analytics** et tableaux de bord

## 🛠️ Développement

### Structure du Projet
```
lacaravella/
├── caravela/          # Configuration Django
├── products/          # Gestion des produits
├── checkout/          # Système de commande
├── users/             # Profils utilisateurs
├── analytics/         # Tableaux de bord
├── templates/         # Templates HTML
├── static/           # Fichiers statiques
└── docs/            # Documentation
```

### Commandes Utiles

```bash
# Vérifier la configuration
python manage.py check

# Créer des migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Créer un superuser
python manage.py createsuperuser

# Collecter les fichiers statiques
python manage.py collectstatic

# Lancer les tests
python manage.py test

# Shell Django
python manage.py shell
```

## 🎨 Personnalisation

### Modifier le Design
- **CSS** : `static/css/main.css`
- **JavaScript** : `static/js/main.js`
- **Templates** : `templates/`

### Ajouter des Produits
1. Accéder à l'admin : http://localhost:8000/admin/
2. Se connecter avec le superuser
3. Ajouter des catégories et produits

### Personnaliser les Couleurs
Modifier les variables CSS dans `static/css/main.css` :
```css
:root {
    --caravela-600: #e35d10; /* Couleur principale */
}
```

## 🔒 Sécurité

### Développement
- `DEBUG=True` (activé par défaut)
- Base de données SQLite
- Cache en mémoire

### Production
- `DEBUG=False`
- Base de données PostgreSQL
- Cache Redis
- HTTPS obligatoire

## 📊 Monitoring

### Logs
Les logs sont affichés dans la console du serveur de développement.

### Performance
- Cache intelligent pour les produits
- Lazy loading des images
- Optimisations CSS/JS

## 🚀 Déploiement

### Docker (Recommandé)
```bash
docker-compose up -d
```

### Manuel
```bash
# Installer les dépendances de production
pip install -r requirements.txt

# Configurer la base de données PostgreSQL
# Configurer Redis pour le cache
# Configurer les variables d'environnement

# Collecter les fichiers statiques
python manage.py collectstatic

# Lancer avec Gunicorn
gunicorn caravela.wsgi:application
```

## 📞 Support

### Problèmes Courants

**Erreur Redis** :
- En développement, Redis n'est pas requis
- Le cache utilise la mémoire locale

**Erreur 404** :
- Vérifier que les URLs sont correctes
- Vérifier que les templates existent

**Erreur de migration** :
```bash
python manage.py makemigrations
python manage.py migrate
```

### Ressources
- **Documentation Django** : https://docs.djangoproject.com/
- **Documentation DRF** : https://www.django-rest-framework.org/
- **Documentation Tailwind** : https://tailwindcss.com/

## 🎉 Félicitations !

Votre plateforme La Caravela est maintenant **opérationnelle** !

**Prochaines étapes** :
1. Ajouter des produits via l'admin
2. Personnaliser le design
3. Configurer Stripe pour les paiements
4. Déployer en production

---

**La Caravela** - L'art de la glace artisanale, réinventé pour le digital ! 🍦✨ 