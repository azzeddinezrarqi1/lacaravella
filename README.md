# La Caravela - Plateforme E-commerce Glaces Premium

Une plateforme e-commerce moderne et performante pour La Caravela, spécialisée dans les glaces artisanales premium. Inspirée de MagnumIceCream.com avec une approche personnalisée et une expérience utilisateur exceptionnelle.

## 🍦 Fonctionnalités Principales

### Catalogue & Produits
- **Catalogue produits** avec filtres avancés (parfums, catégories, allergènes)
- **Fiches produits détaillées** avec galeries photos/vidéos
- **Système de personnalisation** des glaces (comme Magnum Create)
- **Recommandations intelligentes** basées sur les préférences utilisateur
- **Gestion des stocks** en temps réel

### Expérience Utilisateur
- **Interface premium** avec design moderne et responsive
- **Personnalisation en temps réel** avec calcul de prix dynamique
- **Système de recherche** avancé avec filtres
- **Liste de souhaits** et historique des commandes
- **Programme de fidélité** avec points et niveaux

### Paiement & Livraison
- **Intégration Stripe** sécurisée pour les paiements
- **Calcul automatique** des frais de port
- **Livraison en points relais** et à domicile
- **Suivi des commandes** en temps réel

### Backoffice Admin
- **Tableaux de bord** analytiques
- **Gestion des stocks** et commandes
- **Système de notifications** automatiques
- **Intégration CRM** (Mailchimp/Klaviyo)

## 🛠️ Stack Technique

### Backend
- **Django 4.2.7** - Framework web robuste
- **Django REST Framework** - API REST performante
- **PostgreSQL** - Base de données relationnelle
- **Redis** - Cache et sessions
- **Celery** - Tâches asynchrones

### Frontend
- **HTML5/CSS3** avec **Tailwind CSS**
- **JavaScript ES6+** avec **Alpine.js**
- **Responsive Design** mobile-first
- **PWA Ready** pour installation mobile

### Infrastructure
- **Docker** - Containerisation
- **AWS/GCP** - Hébergement cloud
- **CI/CD** - Déploiement automatisé
- **CDN** - Optimisation des performances

## 🚀 Installation & Démarrage

### Prérequis
- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose

### Installation Rapide avec Docker

```bash
# Cloner le repository
git clone https://github.com/votre-username/lacaravella.git
cd lacaravella

# Lancer avec Docker Compose
docker-compose up -d

# Créer les migrations et superuser
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

# Accéder à l'application
open http://localhost:8000
```

### Installation Manuelle

```bash
# Cloner le repository
git clone https://github.com/votre-username/lacaravella.git
cd lacaravella

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos configurations

# Configurer la base de données
python manage.py migrate

# Créer un superuser
python manage.py createsuperuser

# Lancer le serveur de développement
python manage.py runserver
```

## 📁 Structure du Projet

```
lacaravella/
├── caravela/                 # Configuration Django principale
│   ├── settings.py          # Configuration de l'application
│   ├── urls.py              # URLs principales
│   └── wsgi.py              # Configuration WSGI
├── products/                # Application produits
│   ├── models.py            # Modèles de données
│   ├── views.py             # Vues et API
│   ├── serializers.py       # Sérialiseurs REST
│   └── urls.py              # URLs produits
├── checkout/                # Application commande/paiement
│   ├── models.py            # Modèles commande
│   ├── views.py             # Vues checkout
│   └── stripe_config.py     # Configuration Stripe
├── users/                   # Application utilisateurs
│   ├── models.py            # Profils utilisateurs
│   └── views.py             # Vues utilisateurs
├── analytics/               # Application analytics
│   └── views.py             # Tableaux de bord
├── templates/               # Templates HTML
│   ├── base.html            # Template de base
│   └── products/            # Templates produits
├── static/                  # Fichiers statiques
│   ├── css/                 # Styles CSS
│   ├── js/                  # JavaScript
│   └── images/              # Images
├── tests/                   # Tests unitaires
├── docker-compose.yml       # Configuration Docker
├── Dockerfile               # Image Docker
├── requirements.txt          # Dépendances Python
└── README.md               # Documentation
```

## 🔧 Configuration

### Variables d'Environnement

Créer un fichier `.env` à la racine du projet :

```env
# Django
SECRET_KEY=votre-clé-secrète-django
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de données
DB_NAME=caravela_db
DB_USER=caravela_user
DB_PASSWORD=caravela_password
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/1

# Stripe (Mode test)
STRIPE_PUBLISHABLE_KEY=pk_test_votre-clé-publique
STRIPE_SECRET_KEY=sk_test_votre-clé-secrète
STRIPE_WEBHOOK_SECRET=whsec_votre-webhook-secret

# Email
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=contact@lacaravela.com

# Klaviyo
KLAVIYO_API_KEY=votre-clé-klaviyo
```

### Configuration Stripe

1. Créer un compte sur [Stripe](https://stripe.com)
2. Récupérer les clés API dans le dashboard
3. Configurer les webhooks pour les événements de paiement
4. Tester avec les cartes de test Stripe

## 🧪 Tests

### Lancer les Tests

```bash
# Tests unitaires
pytest

# Tests avec couverture
pytest --cov=. --cov-report=html

# Tests spécifiques
pytest products/tests/ -v
pytest checkout/tests/ -v

# Tests d'intégration
pytest -m integration

# Tests de performance
pytest -m slow
```

### Structure des Tests

```
tests/
├── products/
│   ├── test_models.py
│   ├── test_views.py
│   └── test_api.py
├── checkout/
│   ├── test_models.py
│   ├── test_views.py
│   └── test_stripe.py
└── users/
    ├── test_models.py
    └── test_views.py
```

## 🚀 Déploiement

### Déploiement sur AWS

```bash
# Configuration AWS CLI
aws configure

# Déployer avec Terraform
terraform init
terraform plan
terraform apply
```

### Déploiement sur GCP

```bash
# Configuration Google Cloud
gcloud auth login
gcloud config set project votre-projet

# Déployer avec Cloud Run
gcloud run deploy lacaravela --source .
```

### CI/CD avec GitHub Actions

Le workflow `.github/workflows/deploy.yml` automatise :
- Tests unitaires
- Tests de sécurité
- Build Docker
- Déploiement automatique

## 📊 Performance & Optimisation

### Cache Redis
- Cache des pages produits : 15 minutes
- Cache des images : 1 an
- Cache API : 5-15 minutes selon le type

### Optimisations Frontend
- Lazy loading des images
- Compression des assets
- CDN pour les fichiers statiques
- Service Worker pour le cache

### Monitoring
- Logs structurés avec JSON
- Métriques de performance
- Alertes automatiques
- Dashboard Grafana

## 🔒 Sécurité

### Mesures Implémentées
- HTTPS obligatoire
- Protection CSRF
- Validation des entrées
- Rate limiting
- Sanitisation des données
- Audit des logs

### Conformité
- RGPD compliant
- PCI DSS pour les paiements
- Certificats SSL/TLS
- Politique de confidentialité

## 🤝 Contribution

### Guidelines
1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

### Standards de Code
- PEP 8 pour Python
- ESLint pour JavaScript
- Prettier pour le formatage
- Tests obligatoires pour les nouvelles fonctionnalités

## 📈 Roadmap

### Phase 1 (Actuel)
- ✅ Catalogue produits
- ✅ Système de personnalisation
- ✅ Paiements Stripe
- ✅ Interface responsive

### Phase 2 (Prochainement)
- 🔄 Application mobile native
- 🔄 Intégration IA pour recommandations
- 🔄 Système de fidélité avancé
- 🔄 Marketplace multi-vendeurs

### Phase 3 (Futur)
- 📋 API publique
- 📋 Intégrations tierces
- 📋 Analytics avancées
- 📋 Expérience VR/AR

## 📞 Support

### Contact
- **Email** : support@lacaravela.com
- **Documentation** : https://docs.lacaravela.com
- **Issues** : https://github.com/votre-username/lacaravella/issues

### Communauté
- **Discord** : https://discord.gg/lacaravela
- **Twitter** : @LaCaravelaTech
- **Blog** : https://blog.lacaravela.com

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🙏 Remerciements

- **Django** pour le framework web robuste
- **Tailwind CSS** pour le design system
- **Stripe** pour les paiements sécurisés
- **Alpine.js** pour l'interactivité légère
- **PostgreSQL** pour la base de données
- **Redis** pour les performances

---

**La Caravela** - L'art de la glace artisanale, réinventé pour le digital. 🍦✨ 