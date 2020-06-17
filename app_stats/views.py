from django.shortcuts import render
from app_websites.models import *
from django.core.paginator import Paginator

from django.db.models import Subquery, OuterRef, DecimalField, IntegerField, Sum, Count

def stats_sales(request):
    return render(request, 'app_stats/sales.html', {})  

def stats_products(request):

    # Product Pagination
    paginator = Paginator(products, 20)
    page = request.GET.get('page')
    items = paginator.get_page(page)

    context = {
        'products' : Product.objects.all(),
    }
    return render(request, 'app_stats/products.html', context)  

def stats_brands(request):
    return render(request, 'app_stats/brands.html', {})  

def stats_suppliers(request):

    # Supplier Stats
    sup_tot_prod = Supplier.objects.all().annotate(sup_tot_prod=Count('product')).filter(pk=OuterRef('pk'))
    sup_buy_pr = Supplier.objects.all().annotate(sup_buy_pr=Sum('product__buy_price')).filter(pk=OuterRef('pk'))
    sup_sell_pr = Supplier.objects.all().annotate(sup_sell_pr=Sum('product__sell_price')).filter(pk=OuterRef('pk'))
    qs = Supplier.objects.annotate (
        sup_tot_prod=Subquery(sup_tot_prod.values('sup_tot_prod'), output_field=DecimalField()),
        sup_buy_pr=Subquery(sup_buy_pr.values('sup_buy_pr'), output_field=DecimalField()),
        sup_sell_pr=Subquery(sup_sell_pr.values('sup_sell_pr'), output_field=DecimalField()),
        
    ).order_by('sort_order')

    context = {
        'supplier_stats' : qs,
        'test' : test,

    }
    return render(request, 'app_stats/suppliers.html', context )  

def stats_customers(request):
    return render(request, 'app_stats/customers.html', {})  
