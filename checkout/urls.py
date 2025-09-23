from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('payment/', views.payment_view, name='payment'),
    path('stripe-webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('order-confirmation/<str:order_number>/', views.order_confirmation, name='order_confirmation'),
] 