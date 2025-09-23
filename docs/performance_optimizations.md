# Guide d'Optimisation des Performances - La Caravela

Ce document détaille les optimisations mises en place pour garantir des temps de chargement rapides et une expérience utilisateur fluide.

## 🚀 Optimisations Backend

### Cache Redis
```python
# Configuration cache dans settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Cache des modèles avec cacheops
CACHEOPS = {
    'products.Product': {'ops': 'all', 'timeout': 60*60},
    'products.Category': {'ops': 'all', 'timeout': 60*60},
}
```

### Optimisations Base de Données
```python
# Requêtes optimisées avec select_related et prefetch_related
products = Product.objects.filter(is_active=True)\
    .select_related('category')\
    .prefetch_related('images', 'flavors', 'allergens')

# Index sur les champs fréquemment utilisés
class Product(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['is_active', 'is_featured']),
            models.Index(fields=['category', 'created_at']),
            models.Index(fields=['base_price']),
        ]
```

### Pagination Intelligente
```python
# Pagination avec cache
@cache_page(60 * 5)
def product_list(request):
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 12)
    return paginator.get_page(page)
```

## 🎨 Optimisations Frontend

### Lazy Loading des Images
```html
<!-- Template avec lazy loading -->
<img src="{{ product.primary_image.url }}" 
     loading="lazy" 
     alt="{{ product.name }}"
     class="product-image">
```

```javascript
// JavaScript pour lazy loading avancé
const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.dataset.src;
            img.classList.remove('lazy');
            observer.unobserve(img);
        }
    });
});

document.querySelectorAll('img[data-src]').forEach(img => {
    imageObserver.observe(img);
});
```

### Compression des Assets
```python
# settings.py - Compression des fichiers statiques
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Configuration WhiteNoise
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ... autres middleware
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Service Worker pour Cache
```javascript
// static/js/sw.js
const CACHE_NAME = 'caravela-v1';
const urlsToCache = [
    '/',
    '/static/css/main.css',
    '/static/js/main.js',
    '/static/images/logo.svg'
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(urlsToCache))
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => response || fetch(event.request))
    );
});
```

## 📊 Optimisations API

### Cache API REST
```python
# Middleware de cache pour l'API
class ProductAPICacheMiddleware:
    def process_response(self, request, response):
        if self.is_product_api_request(request):
            cache_key = self.generate_api_cache_key(request)
            cache.set(cache_key, response, 60 * 5)  # 5 minutes
        return response
```

### Sérialisation Optimisée
```python
# Sérialiseurs avec champs sélectifs
class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'base_price', 'primary_image']
        # Champs minimaux pour les listes
```

## 🖼️ Optimisations Images

### Formats Modernes
```python
# Pillow pour optimisation automatique
from PIL import Image

def optimize_image(image_path):
    img = Image.open(image_path)
    
    # Redimensionner si trop grand
    if img.width > 1200:
        ratio = 1200 / img.width
        new_size = (1200, int(img.height * ratio))
        img = img.resize(new_size, Image.LANCZOS)
    
    # Optimiser la qualité
    img.save(image_path, 'JPEG', quality=85, optimize=True)
```

### Responsive Images
```html
<!-- Images responsives -->
<picture>
    <source media="(min-width: 1200px)" srcset="{{ product.image_1200.url }}">
    <source media="(min-width: 768px)" srcset="{{ product.image_768.url }}">
    <img src="{{ product.image_480.url }}" alt="{{ product.name }}">
</picture>
```

## 🔧 Optimisations Serveur

### Gunicorn Configuration
```python
# gunicorn.conf.py
bind = "0.0.0.0:8000"
workers = 4
worker_class = "gevent"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
preload_app = True
```

### Nginx Configuration
```nginx
# nginx.conf
upstream caravela {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name lacaravela.com;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
    
    # Cache statique
    location /static/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Cache images
    location ~* \.(jpg|jpeg|png|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Proxy vers Django
    location / {
        proxy_pass http://caravela;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📈 Monitoring Performance

### Métriques à Surveiller
```python
# Middleware de performance
class PerformanceMiddleware:
    def process_request(self, request):
        request.start_time = time.time()
    
    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            response['X-Response-Time'] = f"{duration:.3f}s"
            
            # Logger les requêtes lentes
            if duration > 1.0:
                logger.warning(f"Requête lente: {request.path} - {duration:.3f}s")
        
        return response
```

### Outils de Monitoring
- **New Relic** pour APM
- **Sentry** pour les erreurs
- **Google PageSpeed Insights** pour les métriques web
- **Lighthouse CI** pour les audits automatiques

## 🎯 Objectifs de Performance

### Temps de Chargement Cibles
- **Page d'accueil**: < 2 secondes
- **Liste produits**: < 1.5 secondes
- **Fiche produit**: < 2.5 secondes
- **API REST**: < 500ms

### Métriques Core Web Vitals
- **LCP (Largest Contentful Paint)**: < 2.5s
- **FID (First Input Delay)**: < 100ms
- **CLS (Cumulative Layout Shift)**: < 0.1

## 🔄 Optimisations Continues

### Tests de Performance Automatisés
```yaml
# .github/workflows/performance.yml
name: Performance Tests
on: [push, pull_request]

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Lighthouse CI
        uses: treosh/lighthouse-ci-action@v9
        with:
          urls: |
            https://staging.lacaravela.com
            https://staging.lacaravela.com/products/
          uploadArtifacts: true
          temporaryPublicStorage: true
```

### Optimisations Basées sur les Données
- Analyse des logs de performance
- A/B testing des optimisations
- Monitoring des métriques utilisateur
- Optimisations basées sur les patterns d'usage

## 🛠️ Outils Recommandés

### Développement
- **Django Debug Toolbar** pour le profiling
- **django-extensions** pour les commandes de debug
- **django-cacheops** pour le cache automatique

### Production
- **Redis** pour le cache
- **CDN** (Cloudflare/AWS CloudFront) pour les assets
- **Database connection pooling** (PgBouncer)
- **Load balancing** avec HAProxy

### Monitoring
- **Prometheus** + **Grafana** pour les métriques
- **ELK Stack** pour les logs
- **Uptime Robot** pour la disponibilité

---

**Note**: Ces optimisations sont appliquées progressivement et testées en continu pour garantir une expérience utilisateur optimale. 