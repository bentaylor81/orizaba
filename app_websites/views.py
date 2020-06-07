from django.shortcuts import render, redirect
from django.db.models import Sum
from .models import *
from .filters import *
from django.contrib.auth.decorators import login_required
from app_users.decorators import unauthenticated_user, allowed_users
from django.core.paginator import Paginator
from .forms import OrderNoteForm
from django.contrib import messages

def home(request):
    return render(request, 'app_websites/orders.html' )

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def orders(request):

    orders = Order.objects.all()
    # Order Filtering
    orderFilter = OrderFilter(request.GET, queryset=orders)
    orders = orderFilter.qs
    # Order Pagination
    paginator = Paginator(orders, 20)
    page = request.GET.get('page')
    orders = paginator.get_page(page)

    context = { 
        'orders' : orders,
        'orderFilter' : OrderFilter()
        }
            
    return render(request, 'app_websites/orders.html', context )

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def order_view(request, id):

    items_total = OrderItem.objects.filter(order_id__order_no=id).aggregate(Sum('total_price'))['total_price__sum']
    order = Order.objects.get(order_no=id)
    postage = order.delivery_price
    total_ex_vat = items_total + postage
    vat = round(float(total_ex_vat) * 0.2, 2)
    total_inc_vat = round(float(total_ex_vat) + vat, 2)

    context = {
        'order' : order,
        'order_items' : OrderItem.objects.filter(order_id__order_no=id),
        'notes' : OrderNote.objects.filter(order_id__order_no=id),
        'items_total' : items_total,
        'postage' : postage,
        'vat' : vat,
        'total_ex_vat' : total_ex_vat,
        'total_inc_vat' : total_inc_vat, 
        'current_user' : request.user,
        }

    if request.method == 'POST':
        form = OrderNoteForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, ('Note has been added'))
            return render(request, 'app_websites/order-view.html', context)
        else: 
            messages.error(request, ('Note cannot be blank'))
            return render(request, 'app_websites/order-view.html', context)
    else:
        return render(request, 'app_websites/order-view.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):

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
        'productFilter' : ProductFilter()
        }
    return render(request, 'app_websites/products.html', context )

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def product_view(request, id):

    context = { 
        'product' : Product.objects.get(product_id=id),
        'product_orders' : OrderItem.objects.filter(product_id__product_id=id),
        'product_total_price' : OrderItem.objects.filter(product_id__product_id=id).aggregate(Sum('total_price'))['total_price__sum']
        }
    return render(request, 'app_websites/product-view.html', context )

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def suppliers(request):

    context = { 
        'suppliers' : Supplier.objects.all().order_by('sort_order'),
        'products' : Product.objects.all(),
        }
    return render(request, 'app_websites/suppliers.html', context )

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def supplier_view(request, path):

    products = Product.objects.filter(supplier__path=path).order_by('sell_price')
    # Supplier Product Filtering
    supplierproductFilter = SupplierProductFilter(request.GET, queryset=products)
    products = supplierproductFilter.qs
    # Supplier Product Pagination
    paginator = Paginator(products, 20)
    page = request.GET.get('page')
    items = paginator.get_page(page)

    context = {
        'supplier' : Supplier.objects.get(path=path),
        'items' : items, 
        'products' : products,
        'supplierproductFilter' : SupplierProductFilter(),
        'cheap_product' : Product.objects.filter(supplier__path=path).order_by('sell_price')[0],
        'expen_product' : Product.objects.filter(supplier__path=path).order_by('-sell_price')[0],
        'product_count' : Product.objects.filter(supplier__path=path).count(),
        }

    return render(request, 'app_websites/supplier-view.html', context )

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def brands(request):

    context = { 
        'brands' : Brand.objects.all(),
        }
    return render(request, 'app_websites/brands.html', context )

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customers(request):

    context = { 
        'customers' : Customer.objects.all(),
        }
    return render(request, 'app_websites/customers.html', context )