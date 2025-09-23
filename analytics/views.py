from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def dashboard_view(request):
    """Tableau de bord principal"""
    return render(request, 'analytics/dashboard.html')

@staff_member_required
def sales_view(request):
    """Analytics des ventes"""
    return render(request, 'analytics/sales.html')

@staff_member_required
def products_analytics(request):
    """Analytics des produits"""
    return render(request, 'analytics/products.html')

@staff_member_required
def customers_analytics(request):
    """Analytics des clients"""
    return render(request, 'analytics/customers.html')
