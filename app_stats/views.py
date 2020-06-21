from django.shortcuts import render, redirect
from app_websites.models import *
from app_stats.models import *
from app_websites.filters import *
from django.core.paginator import Paginator
from django.db.models import Subquery, OuterRef, DecimalField, IntegerField, Sum, Count

def stats_sales_day(request):

    context = {
        'daily_sales' : Day.objects.all(),
    } 

    return render(request, 'app_stats/sales-day.html', context )  

def stats_sales_mon(request):

    context = {
        'monthly_sales' : Month.objects.all(),
    } 

    return render(request, 'app_stats/sales-mon.html', context )  

def stats_sales_year(request):

    context = {
        'yearly_sales' : Year.objects.all(),
    } 

    return render(request, 'app_stats/sales-year.html', context )  

def stats_prod_fin(request):

    products = Product.objects.all()
    # Product Filtering
    productFilter = ProductFilter(request.GET, queryset=products)
    products = productFilter.qs

    # Product Pagination
    paginator = Paginator(products, 50)
    page = request.GET.get('page')
    items = paginator.get_page(page)

    context = {
        'products' : products,
        'items' : items,
        'productFilter' : ProductFilter(),
    }
    return render(request, 'app_stats/prod-fin.html', context)  

def stats_prod_sto(request):
    return render(request, 'app_stats/prod-sto.html', {})  

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
    }
    return render(request, 'app_stats/suppliers.html', context )  

def stats_customers(request):
    return render(request, 'app_stats/customers.html', {})  
