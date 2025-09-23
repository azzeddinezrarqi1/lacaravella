from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('sales/', views.sales_view, name='sales'),
    path('products/', views.products_analytics, name='products'),
    path('customers/', views.customers_analytics, name='customers'),
] 