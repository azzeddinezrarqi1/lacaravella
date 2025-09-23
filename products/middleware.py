import hashlib
import json
from django.core.cache import cache
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings


class ProductCacheMiddleware(MiddlewareMixin):
    """
    Middleware de cache pour les fiches produits
    Cache les pages produit avec une clé basée sur l'URL et les paramètres
    """
    
    def process_request(self, request):
        # Vérifier si c'est une page produit
        if self.is_product_page(request):
            cache_key = self.generate_cache_key(request)
            cached_response = cache.get(cache_key)
            
            if cached_response:
                return cached_response
        
        return None
    
    def process_response(self, request, response):
        # Vérifier si c'est une page produit et si la réponse est valide
        if (self.is_product_page(request) and 
            response.status_code == 200 and 
            'text/html' in response.get('Content-Type', '')):
            
            cache_key = self.generate_cache_key(request)
            
            # Ne pas mettre en cache les réponses pour les utilisateurs connectés
            # ou si le cache est désactivé
            if (not request.user.is_authenticated and 
                getattr(settings, 'ENABLE_PRODUCT_CACHE', True)):
                
                # Ajouter des en-têtes pour indiquer que c'est du cache
                response['X-Cache'] = 'HIT'
                response['X-Cache-Key'] = cache_key
                
                # Mettre en cache pour 15 minutes
                cache.set(cache_key, response, 60 * 15)
        
        return response
    
    def is_product_page(self, request):
        """Vérifier si c'est une page produit"""
        return (
            request.path.startswith('/products/product/') or
            request.path.startswith('/products/category/') or
            request.path == '/products/'
        )
    
    def generate_cache_key(self, request):
        """Générer une clé de cache unique"""
        # Base de la clé : URL + méthode HTTP
        key_parts = [
            request.path,
            request.method,
        ]
        
        # Ajouter les paramètres GET pertinents
        relevant_params = ['category', 'flavor', 'allergen', 'price_min', 'price_max', 'sort']
        for param in relevant_params:
            if param in request.GET:
                key_parts.append(f"{param}={request.GET[param]}")
        
        # Ajouter la langue si disponible
        if hasattr(request, 'LANGUAGE_CODE'):
            key_parts.append(f"lang={request.LANGUAGE_CODE}")
        
        # Créer une clé unique
        key_string = '|'.join(key_parts)
        return f"product_cache:{hashlib.md5(key_string.encode()).hexdigest()}"


class ProductImageOptimizationMiddleware(MiddlewareMixin):
    """
    Middleware pour optimiser les images des produits
    Ajoute des en-têtes de cache appropriés pour les images
    """
    
    def process_response(self, request, response):
        # Vérifier si c'est une image de produit
        if self.is_product_image(request):
            # Ajouter des en-têtes de cache pour les images
            response['Cache-Control'] = 'public, max-age=31536000'  # 1 an
            response['Expires'] = 'Thu, 31 Dec 2037 23:55:55 GMT'
            
            # Ajouter des en-têtes pour l'optimisation
            response['X-Image-Optimized'] = 'true'
        
        return response
    
    def is_product_image(self, request):
        """Vérifier si c'est une image de produit"""
        return (
            request.path.startswith('/media/products/') or
            request.path.startswith('/media/categories/') or
            request.path.startswith('/media/customizations/')
        )


class ProductAPICacheMiddleware(MiddlewareMixin):
    """
    Middleware de cache pour l'API des produits
    Cache les réponses API avec une durée adaptée
    """
    
    def process_request(self, request):
        # Vérifier si c'est une requête API produit
        if self.is_product_api_request(request):
            cache_key = self.generate_api_cache_key(request)
            cached_response = cache.get(cache_key)
            
            if cached_response:
                return cached_response
        
        return None
    
    def process_response(self, request, response):
        # Vérifier si c'est une réponse API produit valide
        if (self.is_product_api_request(request) and 
            response.status_code == 200 and 
            'application/json' in response.get('Content-Type', '')):
            
            cache_key = self.generate_api_cache_key(request)
            
            # Mettre en cache pour 5 minutes pour les listes, 15 minutes pour les détails
            cache_duration = 60 * 15 if 'detail' in request.path else 60 * 5
            cache.set(cache_key, response, cache_duration)
        
        return response
    
    def is_product_api_request(self, request):
        """Vérifier si c'est une requête API produit"""
        return (
            request.path.startswith('/products/api/') and
            request.method == 'GET'
        )
    
    def generate_api_cache_key(self, request):
        """Générer une clé de cache pour l'API"""
        key_parts = [
            'api',
            request.path,
            request.method,
        ]
        
        # Ajouter les paramètres de requête
        if request.GET:
            key_parts.append(json.dumps(dict(request.GET), sort_keys=True))
        
        # Ajouter la langue
        if hasattr(request, 'LANGUAGE_CODE'):
            key_parts.append(f"lang={request.LANGUAGE_CODE}")
        
        key_string = '|'.join(key_parts)
        return f"product_api_cache:{hashlib.md5(key_string.encode()).hexdigest()}"


class ProductPerformanceMiddleware(MiddlewareMixin):
    """
    Middleware pour mesurer les performances des pages produit
    """
    
    def process_request(self, request):
        if self.is_product_page(request):
            request.start_time = time.time()
    
    def process_response(self, request, response):
        if hasattr(request, 'start_time') and self.is_product_page(request):
            duration = time.time() - request.start_time
            
            # Ajouter le temps de réponse dans les en-têtes
            response['X-Response-Time'] = f"{duration:.3f}s"
            
            # Logger les performances lentes
            if duration > 1.0:  # Plus d'1 seconde
                import logging
                logger = logging.getLogger('performance')
                logger.warning(
                    f"Page produit lente: {request.path} - {duration:.3f}s"
                )
        
        return response
    
    def is_product_page(self, request):
        """Vérifier si c'est une page produit"""
        return (
            request.path.startswith('/products/') or
            request.path == '/'
        )


# Import time pour le middleware de performance
import time 