from django.contrib import admin
from .models import Category, Product, Flavor, Allergen, ProductFlavor, ProductImage, CustomizationOption, ProductReview

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']
    list_editable = ['is_active', 'order']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'product_type', 'base_price', 'is_active', 'is_featured', 'created_at']
    list_filter = ['category', 'product_type', 'is_active', 'is_featured', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['allergens', 'flavors']
    list_editable = ['is_active', 'is_featured']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Flavor)
class FlavorAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_active', 'order']

@admin.register(Allergen)
class AllergenAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_active']

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'alt_text', 'is_primary', 'order', 'created_at']
    list_filter = ['is_primary', 'created_at']
    list_editable = ['is_primary', 'order']

@admin.register(CustomizationOption)
class CustomizationOptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'option_type', 'is_active', 'order']
    list_filter = ['option_type', 'is_active']
    list_editable = ['is_active', 'order']

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'is_approved', 'created_at']
    list_filter = ['rating', 'is_approved', 'created_at']
    search_fields = ['product__name', 'user__username', 'comment']
    list_editable = ['is_approved']
