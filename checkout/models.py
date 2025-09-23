from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid
from products.models import CustomizationOption


class Address(models.Model):
    """Adresse de livraison/facturation"""
    ADDRESS_TYPES = [
        ('shipping', 'Livraison'),
        ('billing', 'Facturation'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name="Utilisateur")
    address_type = models.CharField(max_length=20, choices=ADDRESS_TYPES, default='shipping', verbose_name="Type d'adresse")
    is_default = models.BooleanField(default=False, verbose_name="Adresse par défaut")
    
    first_name = models.CharField(max_length=50, verbose_name="Prénom")
    last_name = models.CharField(max_length=50, verbose_name="Nom")
    company = models.CharField(max_length=100, blank=True, verbose_name="Société")
    address_line_1 = models.CharField(max_length=255, verbose_name="Adresse")
    address_line_2 = models.CharField(max_length=255, blank=True, verbose_name="Complément d'adresse")
    city = models.CharField(max_length=100, verbose_name="Ville")
    state = models.CharField(max_length=100, blank=True, verbose_name="État/Région")
    postal_code = models.CharField(max_length=20, verbose_name="Code postal")
    country = models.CharField(max_length=100, default="France", verbose_name="Pays")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Adresse"
        verbose_name_plural = "Adresses"
        ordering = ['-is_default', '-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.city}"

    def save(self, *args, **kwargs):
        if self.is_default:
            # Désactiver les autres adresses par défaut du même type pour cet utilisateur
            Address.objects.filter(
                user=self.user,
                address_type=self.address_type,
                is_default=True
            ).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)


class Cart(models.Model):
    """Panier d'achat"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts', verbose_name="Utilisateur")
    session_key = models.CharField(max_length=40, blank=True, verbose_name="Clé de session")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Panier"
        verbose_name_plural = "Paniers"

    def __str__(self):
        return f"Panier de {self.user.username if self.user else 'Anonyme'}"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def total(self):
        return self.subtotal + self.shipping_cost - self.discount_amount

    @property
    def shipping_cost(self):
        # Logique de calcul des frais de port
        if self.subtotal >= 500:  # Livraison gratuite au-dessus de 500 MAD
            return Decimal('0.00')
        return Decimal('59.90')

    @property
    def discount_amount(self):
        return Decimal('0.00')  # À implémenter avec les codes promo


class CartItem(models.Model):
    """Article dans le panier"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name="Panier")
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, verbose_name="Produit")
    flavor = models.ForeignKey('products.Flavor', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Parfum")
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], verbose_name="Quantité")
    
    # Personnalisations
    customizations = models.JSONField(default=dict, blank=True, verbose_name="Personnalisations")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Article du panier"
        verbose_name_plural = "Articles du panier"
        unique_together = ['cart', 'product', 'flavor']

    def __str__(self):
        flavor_text = f" - {self.flavor.name}" if self.flavor else ""
        return f"{self.product.name}{flavor_text} x{self.quantity}"

    @property
    def unit_price(self):
        base_price = self.product.current_price
        if self.flavor:
            try:
                product_flavor = self.product.productflavor_set.get(flavor=self.flavor)
                base_price += product_flavor.price_modifier
            except:
                pass
        
        # Ajouter le prix des personnalisations
        customization_price = Decimal('0.00')
        for customization_id, details in self.customizations.items():
            try:
                customization = CustomizationOption.objects.get(id=customization_id)
                customization_price += customization.price * details.get('quantity', 1)
            except:
                pass
        
        return base_price + customization_price

    @property
    def total_price(self):
        return self.unit_price * self.quantity


class Order(models.Model):
    """Commande"""
    ORDER_STATUS = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmée'),
        ('processing', 'En préparation'),
        ('shipped', 'Expédiée'),
        ('delivered', 'Livrée'),
        ('cancelled', 'Annulée'),
        ('refunded', 'Remboursée'),
    ]

    PAYMENT_STATUS = [
        ('pending', 'En attente'),
        ('paid', 'Payée'),
        ('failed', 'Échouée'),
        ('refunded', 'Remboursée'),
    ]

    order_number = models.CharField(max_length=20, unique=True, verbose_name="Numéro de commande")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name="Utilisateur")
    
    # Statuts
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending', verbose_name="Statut de commande")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending', verbose_name="Statut de paiement")
    
    # Adresses
    shipping_address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='shipping_orders', verbose_name="Adresse de livraison")
    billing_address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='billing_orders', verbose_name="Adresse de facturation")
    
    # Montants
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Sous-total")
    shipping_cost = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Frais de port")
    discount_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name="Montant de la remise")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total")
    
    # Paiement
    payment_method = models.CharField(max_length=50, blank=True, verbose_name="Méthode de paiement")
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, verbose_name="ID Payment Intent Stripe")
    
    # Livraison
    shipping_method = models.CharField(max_length=50, default="standard", verbose_name="Méthode de livraison")
    tracking_number = models.CharField(max_length=100, blank=True, verbose_name="Numéro de suivi")
    estimated_delivery = models.DateField(blank=True, null=True, verbose_name="Date de livraison estimée")
    
    # Notes
    notes = models.TextField(blank=True, verbose_name="Notes")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ['-created_at']

    def __str__(self):
        return f"Commande {self.order_number}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"CAR{str(uuid.uuid4())[:8].upper()}"
        super().save(*args, **kwargs)

    @property
    def is_paid(self):
        return self.payment_status == 'paid'

    @property
    def can_be_cancelled(self):
        return self.order_status in ['pending', 'confirmed']


class OrderItem(models.Model):
    """Article de commande"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Commande")
    product = models.ForeignKey('products.Product', on_delete=models.PROTECT, verbose_name="Produit")
    flavor = models.ForeignKey('products.Flavor', on_delete=models.PROTECT, blank=True, null=True, verbose_name="Parfum")
    quantity = models.PositiveIntegerField(verbose_name="Quantité")
    unit_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Prix unitaire")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix total")
    customizations = models.JSONField(default=dict, blank=True, verbose_name="Personnalisations")

    class Meta:
        verbose_name = "Article de commande"
        verbose_name_plural = "Articles de commande"

    def __str__(self):
        flavor_text = f" - {self.flavor.name}" if self.flavor else ""
        return f"{self.product.name}{flavor_text} x{self.quantity}"


class Coupon(models.Model):
    """Code promo"""
    COUPON_TYPES = [
        ('percentage', 'Pourcentage'),
        ('fixed', 'Montant fixe'),
        ('free_shipping', 'Livraison gratuite'),
    ]

    code = models.CharField(max_length=20, unique=True, verbose_name="Code")
    description = models.CharField(max_length=200, verbose_name="Description")
    coupon_type = models.CharField(max_length=20, choices=COUPON_TYPES, verbose_name="Type de coupon")
    value = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Valeur")
    
    min_order_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name="Montant minimum de commande")
    max_uses = models.PositiveIntegerField(blank=True, null=True, verbose_name="Utilisations maximum")
    used_count = models.PositiveIntegerField(default=0, verbose_name="Nombre d'utilisations")
    
    valid_from = models.DateTimeField(verbose_name="Valide à partir de")
    valid_until = models.DateTimeField(verbose_name="Valide jusqu'au")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"

    def __str__(self):
        return self.code

    @property
    def is_valid(self):
        from django.utils import timezone
        now = timezone.now()
        return (
            self.is_active and
            self.valid_from <= now <= self.valid_until and
            (self.max_uses is None or self.used_count < self.max_uses)
        )

    def apply_to_order(self, order):
        """Appliquer le coupon à une commande"""
        if not self.is_valid:
            return False
        
        if order.subtotal < self.min_order_amount:
            return False
        
        if self.coupon_type == 'percentage':
            discount = (order.subtotal * self.value) / 100
        elif self.coupon_type == 'fixed':
            discount = self.value
        elif self.coupon_type == 'free_shipping':
            discount = order.shipping_cost
        else:
            return False
        
        order.discount_amount = discount
        order.total = order.subtotal + order.shipping_cost - discount
        order.save()
        
        self.used_count += 1
        self.save()
        
        return True
