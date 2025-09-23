from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('orders/', views.orders_view, name='orders'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
] 