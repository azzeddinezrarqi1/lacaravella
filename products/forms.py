from django import forms
from .models import Product, ProductImage


class ProductForm(forms.ModelForm):
    primary_image = forms.ImageField(required=False, help_text="Image principale du produit")

    class Meta:
        model = Product
        fields = [
            'name', 'description', 'short_description', 'category', 'product_type',
            'base_price', 'sale_price', 'is_customizable', 'is_featured', 'is_active',
            'stock_quantity', 'min_order_quantity', 'max_order_quantity',
        ]

    def save(self, commit=True):
        product = super().save(commit=commit)
        image = self.cleaned_data.get('primary_image')
        if commit and image:
            ProductImage.objects.create(product=product, image=image, is_primary=True)
        return product









