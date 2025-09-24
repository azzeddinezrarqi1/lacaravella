# Architecture du Système - La Caravela

## Vue d'ensemble

Système de gestion e-commerce pour glaces artisanales développé en Django.

## Diagramme d'Architecture Simplifié

```mermaid
graph TB
    subgraph "Frontend"
        A[Interface Utilisateur]
        B[Templates HTML]
        C[CSS/JavaScript]
    end
    
    subgraph "Backend Django"
        D[Views]
        E[Models]
        F[URLs]
    end
    
    subgraph "Applications"
        G[Products<br/>Gestion Produits]
        H[Users<br/>Gestion Utilisateurs]
        I[Checkout<br/>E-commerce]
        J[Analytics<br/>Statistiques]
    end
    
    subgraph "Base de Données"
        K[(SQLite/PostgreSQL)]
    end
    
    subgraph "Services Externes"
        L[Stripe<br/>Paiements]
        M[Email<br/>Notifications]
    end
    
    A --> D
    B --> A
    C --> A
    D --> E
    D --> F
    E --> G
    E --> H
    E --> I
    E --> J
    E --> K
    I --> L
    H --> M
```

## Structure des Modules

```mermaid
graph LR
    subgraph "Products App"
        A[Category]
        B[Product]
        C[Flavor]
        D[Allergen]
    end
    
    subgraph "Users App"
        E[UserProfile]
        F[UserActivity]
        G[Notification]
    end
    
    subgraph "Checkout App"
        H[Cart]
        I[Order]
        J[Address]
        K[Coupon]
    end
    
    A --> B
    B --> C
    B --> D
    E --> F
    E --> G
    H --> I
    I --> J
```

## Flux de Données

```mermaid
sequenceDiagram
    participant U as Utilisateur
    participant F as Frontend
    participant B as Backend
    participant DB as Base de Données
    participant S as Stripe
    
    U->>F: Parcourt les produits
    F->>B: Requête produits
    B->>DB: Récupère les données
    DB-->>B: Retourne les produits
    B-->>F: JSON des produits
    F-->>U: Affiche les produits
    
    U->>F: Ajoute au panier
    F->>B: Créer CartItem
    B->>DB: Sauvegarde
    DB-->>B: Confirmation
    B-->>F: Succès
    F-->>U: Produit ajouté
    
    U->>F: Procède au paiement
    F->>B: Créer commande
    B->>S: Initialise paiement
    S-->>B: Payment Intent
    B-->>F: Confirmation
    F-->>U: Page de paiement
```

## Technologies Utilisées

- **Backend**: Django 4.x, Python 3.x
- **Base de données**: SQLite (dev) / PostgreSQL (prod)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **Paiements**: Stripe API
- **Déploiement**: Docker, Docker Compose
- **CI/CD**: GitHub Actions

## Fonctionnalités Implémentées

### 🍦 Gestion des Produits
- Catégories et sous-catégories
- Gestion des parfums et allergènes
- Images multiples par produit
- Système de prix dynamique
- Gestion des stocks

### 👤 Gestion des Utilisateurs
- Profils utilisateur étendus
- Programme de fidélité
- Préférences personnalisées
- Historique des commandes

### 🛒 E-commerce
- Panier persistant
- Processus de commande complet
- Intégration Stripe
- Gestion des adresses
- Codes promo et remises

### 📊 Analytics
- Suivi des activités utilisateur
- Statistiques de vente
- Rapports de performance
