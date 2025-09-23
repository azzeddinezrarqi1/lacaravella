from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta


class UserProfile(models.Model):
    """Profil utilisateur étendu"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="Utilisateur")
    
    # Informations personnelles
    phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Date de naissance")
    gender = models.CharField(
        max_length=10,
        choices=[('M', 'Homme'), ('F', 'Femme'), ('O', 'Autre')],
        blank=True,
        verbose_name="Genre"
    )
    
    # Préférences
    favorite_flavors = models.ManyToManyField('products.Flavor', blank=True, verbose_name="Parfums préférés")
    dietary_restrictions = models.ManyToManyField('products.Allergen', blank=True, verbose_name="Restrictions alimentaires")
    newsletter_subscription = models.BooleanField(default=True, verbose_name="Abonnement newsletter")
    
    # Programme de fidélité
    loyalty_points = models.PositiveIntegerField(default=0, verbose_name="Points de fidélité")
    loyalty_tier = models.CharField(
        max_length=20,
        choices=[
            ('bronze', 'Bronze'),
            ('silver', 'Argent'),
            ('gold', 'Or'),
            ('platinum', 'Platine'),
        ],
        default='bronze',
        verbose_name="Niveau de fidélité"
    )
    
    # Statistiques
    total_orders = models.PositiveIntegerField(default=0, verbose_name="Total des commandes")
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Total dépensé")
    last_order_date = models.DateTimeField(blank=True, null=True, verbose_name="Date de dernière commande")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Profil utilisateur"
        verbose_name_plural = "Profils utilisateurs"

    def __str__(self):
        return f"Profil de {self.user.username}"

    @property
    def age(self):
        if self.birth_date:
            return (timezone.now().date() - self.birth_date).days // 365
        return None

    def add_loyalty_points(self, points):
        """Ajouter des points de fidélité"""
        self.loyalty_points += points
        self.update_loyalty_tier()
        self.save()

    def update_loyalty_tier(self):
        """Mettre à jour le niveau de fidélité basé sur les points"""
        if self.loyalty_points >= 1000:
            self.loyalty_tier = 'platinum'
        elif self.loyalty_points >= 500:
            self.loyalty_tier = 'gold'
        elif self.loyalty_points >= 200:
            self.loyalty_tier = 'silver'
        else:
            self.loyalty_tier = 'bronze'

    def get_loyalty_discount(self):
        """Obtenir la remise de fidélité"""
        discounts = {
            'bronze': 0,
            'silver': 5,
            'gold': 10,
            'platinum': 15,
        }
        return discounts.get(self.loyalty_tier, 0)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Créer automatiquement un profil utilisateur"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Sauvegarder le profil utilisateur"""
    instance.profile.save()


class UserActivity(models.Model):
    """Activité utilisateur pour analytics"""
    ACTIVITY_TYPES = [
        ('login', 'Connexion'),
        ('product_view', 'Vue produit'),
        ('add_to_cart', 'Ajout au panier'),
        ('purchase', 'Achat'),
        ('review', 'Avis'),
        ('wishlist_add', 'Ajout liste de souhaits'),
        ('coupon_used', 'Utilisation coupon'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities', verbose_name="Utilisateur")
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES, verbose_name="Type d'activité")
    description = models.CharField(max_length=255, verbose_name="Description")
    metadata = models.JSONField(default=dict, blank=True, verbose_name="Métadonnées")
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="Adresse IP")
    user_agent = models.TextField(blank=True, verbose_name="User Agent")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Activité utilisateur"
        verbose_name_plural = "Activités utilisateurs"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.get_activity_type_display()}"


class ReferralProgram(models.Model):
    """Programme de parrainage"""
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals_sent', verbose_name="Parrain")
    referred = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals_received', verbose_name="Filleul")
    referral_code = models.CharField(max_length=20, unique=True, verbose_name="Code de parrainage")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    reward_claimed = models.BooleanField(default=False, verbose_name="Récompense réclamée")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Parrainage"
        verbose_name_plural = "Parrainages"
        unique_together = ['referrer', 'referred']

    def __str__(self):
        return f"{self.referrer.username} → {self.referred.username}"


class Notification(models.Model):
    """Notifications utilisateur"""
    NOTIFICATION_TYPES = [
        ('order_status', 'Statut de commande'),
        ('promotion', 'Promotion'),
        ('loyalty', 'Fidélité'),
        ('newsletter', 'Newsletter'),
        ('system', 'Système'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', verbose_name="Utilisateur")
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, verbose_name="Type de notification")
    title = models.CharField(max_length=200, verbose_name="Titre")
    message = models.TextField(verbose_name="Message")
    is_read = models.BooleanField(default=False, verbose_name="Lu")
    is_sent = models.BooleanField(default=False, verbose_name="Envoyé")
    metadata = models.JSONField(default=dict, blank=True, verbose_name="Métadonnées")
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(blank=True, null=True, verbose_name="Lu le")

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    def mark_as_read(self):
        """Marquer comme lu"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()


class UserPreference(models.Model):
    """Préférences utilisateur"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences', verbose_name="Utilisateur")
    
    # Préférences de communication
    email_notifications = models.BooleanField(default=True, verbose_name="Notifications email")
    sms_notifications = models.BooleanField(default=False, verbose_name="Notifications SMS")
    push_notifications = models.BooleanField(default=True, verbose_name="Notifications push")
    
    # Préférences de livraison
    preferred_shipping_method = models.CharField(
        max_length=20,
        choices=[
            ('standard', 'Livraison standard'),
            ('express', 'Livraison express'),
            ('pickup', 'Point relais'),
        ],
        default='standard',
        verbose_name="Méthode de livraison préférée"
    )
    
    # Préférences de paiement
    save_payment_info = models.BooleanField(default=False, verbose_name="Sauvegarder les informations de paiement")
    
    # Préférences de personnalisation
    default_ice_cream_size = models.CharField(
        max_length=20,
        choices=[
            ('small', 'Petite'),
            ('medium', 'Moyenne'),
            ('large', 'Grande'),
        ],
        default='medium',
        verbose_name="Taille de glace par défaut"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Préférence utilisateur"
        verbose_name_plural = "Préférences utilisateur"

    def __str__(self):
        return f"Préférences de {self.user.username}"
