from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
import uuid


class Category(models.Model):
    """Catégorie de produits (ex: Glaces, Sorbets, Crèmes glacées)"""
    name = models.CharField(max_length=100, verbose_name="Nom")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name="Description")
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name="Image")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:category_detail', kwargs={'slug': self.slug})


class Allergen(models.Model):
    """Allergènes (ex: Lait, Œufs, Fruits à coque)"""
    name = models.CharField(max_length=50, verbose_name="Nom")
    icon = models.CharField(max_length=50, blank=True, verbose_name="Icône")
    description = models.TextField(blank=True, verbose_name="Description")
    is_active = models.BooleanField(default=True, verbose_name="Actif")

    class Meta:
        verbose_name = "Allergène"
        verbose_name_plural = "Allergènes"
        ordering = ['name']

    def __str__(self):
        return self.name


class Flavor(models.Model):
    """Parfums disponibles"""
    name = models.CharField(max_length=100, verbose_name="Nom")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name="Description")
    color = models.CharField(max_length=7, default="#000000", verbose_name="Couleur")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")

    class Meta:
        verbose_name = "Parfum"
        verbose_name_plural = "Parfums"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    """Produit principal (glace)"""
    PRODUCT_TYPES = [
        ('ice_cream', 'Crème glacée'),
        ('sorbet', 'Sorbet'),
        ('frozen_yogurt', 'Yaourt glacé'),
        ('gelato', 'Gelato'),
    ]

    name = models.CharField(max_length=200, verbose_name="Nom")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(verbose_name="Description")
    short_description = models.CharField(max_length=255, blank=True, verbose_name="Description courte")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Image")
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Catégorie")
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPES, default='ice_cream', verbose_name="Type de produit")
    
    base_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Prix de base")
    sale_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name="Prix en promotion")
    
    allergens = models.ManyToManyField(Allergen, blank=True, verbose_name="Allergènes")
    flavors = models.ManyToManyField(Flavor, through='ProductFlavor', verbose_name="Parfums disponibles")
    
    is_customizable = models.BooleanField(default=True, verbose_name="Personnalisable")
    is_featured = models.BooleanField(default=False, verbose_name="En vedette")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name="Stock")
    min_order_quantity = models.PositiveIntegerField(default=1, verbose_name="Quantité minimum")
    max_order_quantity = models.PositiveIntegerField(default=50, verbose_name="Quantité maximum")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'slug': self.slug})

    @property
    def current_price(self):
        return self.sale_price if self.sale_price else self.base_price

    @property
    def is_on_sale(self):
        return bool(self.sale_price and self.sale_price < self.base_price)

    @property
    def discount_percentage(self):
        if self.is_on_sale:
            return int(((self.base_price - self.sale_price) / self.base_price) * 100)
        return 0


class ProductFlavor(models.Model):
    """Relation entre produit et parfums avec prix spécifique"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produit")
    flavor = models.ForeignKey(Flavor, on_delete=models.CASCADE, verbose_name="Parfum")
    price_modifier = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name="Modificateur de prix")
    is_available = models.BooleanField(default=True, verbose_name="Disponible")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")

    class Meta:
        verbose_name = "Parfum de produit"
        verbose_name_plural = "Parfums de produit"
        unique_together = ['product', 'flavor']
        ordering = ['order', 'flavor__name']

    def __str__(self):
        return f"{self.product.name} - {self.flavor.name}"


class ProductImage(models.Model):
    """Images des produits"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="Produit")
    image = models.ImageField(upload_to='products/', verbose_name="Image")
    alt_text = models.CharField(max_length=200, blank=True, verbose_name="Texte alternatif")
    is_primary = models.BooleanField(default=False, verbose_name="Image principale")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Image de produit"
        verbose_name_plural = "Images de produit"
        ordering = ['is_primary', 'order', 'created_at']

    def __str__(self):
        return f"Image de {self.product.name}"


class CustomizationOption(models.Model):
    """Options de personnalisation (ex: Toppings, Sauces)"""
    OPTION_TYPES = [
        ('topping', 'Topping'),
        ('sauce', 'Sauce'),
        ('size', 'Taille'),
        ('container', 'Contenant'),
    ]

    name = models.CharField(max_length=100, verbose_name="Nom")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    option_type = models.CharField(max_length=20, choices=OPTION_TYPES, verbose_name="Type d'option")
    description = models.TextField(blank=True, verbose_name="Description")
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name="Prix")
    image = models.ImageField(upload_to='customizations/', blank=True, null=True, verbose_name="Image")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    max_selections = models.PositiveIntegerField(default=1, verbose_name="Sélections maximum")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")

    class Meta:
        verbose_name = "Option de personnalisation"
        verbose_name_plural = "Options de personnalisation"
        ordering = ['option_type', 'order', 'name']

    def __str__(self):
        return f"{self.get_option_type_display()} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductReview(models.Model):
    """Avis clients sur les produits"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name="Produit")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilisateur")
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Note"
    )
    title = models.CharField(max_length=200, verbose_name="Titre")
    comment = models.TextField(verbose_name="Commentaire")
    is_approved = models.BooleanField(default=False, verbose_name="Approuvé")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Avis produit"
        verbose_name_plural = "Avis produits"
        unique_together = ['product', 'user']
        ordering = ['-created_at']

    def __str__(self):
        return f"Avis de {self.user.username} sur {self.product.name}"


class Wishlist(models.Model):
    """Liste de souhaits des utilisateurs"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist', verbose_name="Utilisateur")
    products = models.ManyToManyField(Product, verbose_name="Produits")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Liste de souhaits"
        verbose_name_plural = "Listes de souhaits"

    def __str__(self):
        return f"Liste de souhaits de {self.user.username}"
