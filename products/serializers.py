from rest_framework import serializers
from .models import (
    Product, Category, Flavor, Allergen, CustomizationOption,
    ProductReview, ProductImage, ProductFlavor
)
from django.db.models import Avg


class AllergenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergen
        fields = ['id', 'name', 'icon', 'description']


class FlavorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flavor
        fields = ['id', 'name', 'slug', 'description', 'color']


class ProductFlavorSerializer(serializers.ModelSerializer):
    flavor = FlavorSerializer(read_only=True)
    
    class Meta:
        model = ProductFlavor
        fields = ['flavor', 'price_modifier', 'is_available']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_primary', 'order']


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'products_count']
    
    def get_products_count(self, obj):
        return obj.products.filter(is_active=True).count()


class CustomizationOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomizationOption
        fields = [
            'id', 'name', 'slug', 'option_type', 'description',
            'price', 'image', 'max_selections', 'order'
        ]


class ProductReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_avatar = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductReview
        fields = [
            'id', 'rating', 'title', 'comment', 'user_name',
            'user_avatar', 'created_at'
        ]
        read_only_fields = ['user', 'is_approved']
    
    def get_user_avatar(self, obj):
        # Retourner l'avatar de l'utilisateur si disponible
        return None  # À implémenter avec un système d'avatars


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    allergens = AllergenSerializer(many=True, read_only=True)
    flavors = ProductFlavorSerializer(source='productflavor_set', many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    reviews_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    primary_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'short_description',
            'category', 'product_type', 'base_price', 'sale_price',
            'current_price', 'is_on_sale', 'discount_percentage',
            'allergens', 'flavors', 'images', 'primary_image',
            'is_customizable', 'is_featured', 'stock_quantity',
            'reviews_count', 'average_rating', 'created_at'
        ]
    
    def get_reviews_count(self, obj):
        return obj.reviews.filter(is_approved=True).count()
    
    def get_average_rating(self, obj):
        avg = obj.reviews.filter(is_approved=True).aggregate(Avg('rating'))
        return avg['rating__avg'] if avg['rating__avg'] else 0
    
    def get_primary_image(self, obj):
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            return ProductImageSerializer(primary_image).data
        return None


class ProductDetailSerializer(ProductSerializer):
    """Sérialiseur détaillé pour les pages produit"""
    reviews = ProductReviewSerializer(many=True, read_only=True)
    customization_options = serializers.SerializerMethodField()
    
    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ['reviews', 'customization_options']
    
    def get_customization_options(self, obj):
        options = CustomizationOption.objects.filter(is_active=True)
        return CustomizationOptionSerializer(options, many=True).data


# Sérialiseurs pour les formulaires
class ProductReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = ['product', 'rating', 'title', 'comment']
    
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("La note doit être entre 1 et 5")
        return value
    
    def validate(self, data):
        # Vérifier que l'utilisateur n'a pas déjà laissé un avis pour ce produit
        user = self.context['request'].user
        product = data['product']
        
        if ProductReview.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError("Vous avez déjà laissé un avis pour ce produit")
        
        return data


# Sérialiseurs pour les filtres
class ProductFilterSerializer(serializers.Serializer):
    category = serializers.CharField(required=False)
    flavor = serializers.CharField(required=False)
    allergen = serializers.IntegerField(required=False)
    price_min = serializers.DecimalField(max_digits=8, decimal_places=2, required=False)
    price_max = serializers.DecimalField(max_digits=8, decimal_places=2, required=False)
    sort = serializers.CharField(required=False)
    page = serializers.IntegerField(required=False, min_value=1)


# Sérialiseurs pour la personnalisation
class CustomizationRequestSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    flavor_id = serializers.IntegerField(required=False, allow_null=True)
    customizations = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        default=list
    )


class CustomizationResponseSerializer(serializers.Serializer):
    base_price = serializers.DecimalField(max_digits=8, decimal_places=2)
    flavor_price_modifier = serializers.DecimalField(max_digits=8, decimal_places=2)
    customization_price = serializers.DecimalField(max_digits=8, decimal_places=2)
    total_price = serializers.DecimalField(max_digits=8, decimal_places=2)
    customizations = serializers.ListField(
        child=serializers.DictField(),
        required=False
    ) 