from django.conf import settings
from django.shortcuts import render, redirect
from django.db.models import Subquery, OuterRef, DecimalField, IntegerField, Sum, Count
from app_websites.models import *
from app_stats.models import *
from app_orders.models import *
from .filters import *
from django.contrib.auth.decorators import login_required
from app_users.decorators import unauthenticated_user, allowed_users
from django.core.paginator import Paginator
from django.contrib import messages
from django.views.generic import View, ListView
from django_filters.views import FilterView
from django.http import HttpResponseRedirect, HttpResponse
from django.views import View
from .forms import ProductLabelForm
import requests
import json
import pdfkit
import wkhtmltopdf


class ProductListView(FilterView):
    template_name = 'products.html'
    model = Product
    paginate_by = 50
    filterset_class = ProductFilter
    strict = False
    form_class = ProductLabelForm

    def post(self, request, *args, **kwargs):
        form = ProductLabelForm(request.POST)
    # Label Parameters from the Form
        sku = form.data['sku']
        product = form.data['product']
        location = form.data['location']
        qty = form.data['qty']
        path = form.data['path']
        
    ### wkhtmltopdf - Generate the label and save to static
        wkhtmltopdf_config = settings.WKHTMLTOPDF_CMD
        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_config)

        options = {
            'copies' : '1',
            'page-width' : '102mm',
            'dpi' : 300,
            'margin-top': '0',
            'margin-right': '0',
            'margin-bottom': '0',
            'margin-left': '0',
        }

    # Create the Label using PDF Kit
        projectUrl = 'http://' + request.get_host() + '/product/label/%s' % sku

    # Generates pdf and creates a file in static
        pdf = pdfkit.from_url(projectUrl, "static/pdf/product-label.pdf", configuration=config, options=options)
        
    # Generates pdf as a download
        #pdf = pdfkit.from_url(projectUrl, False, configuration=config, options=options)
        #response = HttpResponse(pdf, content_type='application/pdf')
        #response['Content-Disposition'] = 'attachment; filename="/label.pdf"'
        #return response

    ### PRINTNODE - Send the Printjob to Print Node ###
        url = settings.PRINTNODE_URL
        auth = settings.PRINTNODE_AUTH
        printer = settings.PRINTNODE_LABEL_PRINTER
        content = "product-label.pdf" 
        copies = qty
        payload = '{"printerId": ' +str(printer)+ ', "title": "Label for: ' +str(sku)+ ' ", "contentType": "pdf_uri", "content":"https://orizaba.herokuapp.com/static/pdf/' +str(content)+ '", "source": "GTS Product Label", "options": {"copies": ' +str(copies)+ '}}'
        headers = {'Content-Type': 'application/json', 'Authorization': auth, }

        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text.encode('utf8'))

        return HttpResponseRedirect(path)

# This Function creates the file which renders the PDF
def generate_label(request, id):
    
    context = { 
            'product': Product.objects.get(sku=id),
        }
    return render(request, 'pdf/label.html', context )

class SupplierListView(ListView):
    template_name = 'suppliers.html'
    model = Supplier

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def home(request):

    return render(request, 'orders.html' )


def product_view(request, id):
    
    product = Product.objects.get(product_id=id)
    if product.stock_qty == 0:
        stock_status = 'no-stock'
    elif 0 < product.stock_qty < 5:
        stock_status = 'low-stock'
    else:
        stock_status = 'good-stock' 

    context = { 
        'product' : product,
        'product_orders' : OrderItem.objects.filter(product_id__product_id=id),
        'product_total_price' : OrderItem.objects.filter(product_id__product_id=id).aggregate(Sum('total_price'))['total_price__sum'],
        'stock_status' : stock_status,
        }
    return render(request, 'product-view.html', context )

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def suppliers(request):

    context = { 
        'suppliers' : Supplier.objects.all().order_by('sort_order'),
        'products' : Product.objects.all(),
        }
    return render(request, 'suppliers.html', context )

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
    # Calculations
    product_count = Product.objects.filter(supplier__path=path).count()

    context = {
        'supplier' : Supplier.objects.get(path=path),
        'items' : items, 
        'products' : products,
        'supplierproductFilter' : SupplierProductFilter(),
        'cheap_product' : Product.objects.filter(supplier__path=path).order_by('sell_price')[0],
        'expen_product' : Product.objects.filter(supplier__path=path).order_by('-sell_price')[0],
        'product_count' : product_count,
        }

    return render(request, 'supplier-view.html', context )

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def brands(request):

    context = { 
        'brands' : Brand.objects.all(),
        }
    return render(request, 'brands.html', context )

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customers(request):

    context = { 
        'customers' : Customer.objects.all(),
        }
    return render(request, 'customers.html', context )

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer_view(request, path):

    # Get the billing email
    customer = Customer.objects.get(customer_id=path)
    billing_email = customer.billing_email

    # Annual Summary Section Subquery
    #ann_spt = Year.objects.filter(order__billing_email=billing_email).annotate(ann_spt=Sum('order__total_price_inc_vat')).filter(pk=OuterRef('pk'))
    #ann_qty = Year.objects.filter(order__billing_email=billing_email).annotate(ann_qty=Sum('order__orderitem__item_qty')).filter(pk=OuterRef('pk'))
    #ann_cnt = Year.objects.filter(order__billing_email=billing_email).annotate(ann_cnt=Count('order')).filter(pk=OuterRef('pk'))
    #qs = Year.objects.annotate (
    #    ann_spt=Subquery(ann_spt.values('ann_spt'), output_field=DecimalField()),
    #    ann_qty=Subquery(ann_qty.values('ann_qty'), output_field=IntegerField()),
    #    ann_cnt=Subquery(ann_cnt.values('ann_cnt'), output_field=IntegerField())
    #).order_by('-year')

    # Notes: 
        # Year field in orders doesn't now exist

    context = {
        'orders' : Order.objects.filter(billing_email=billing_email),
        'order_items' : OrderItem.objects.filter(order_id__billing_email__customer_id=path),
        'first_order' : Order.objects.filter(billing_email=billing_email).order_by('date')[0],
        'last_order' : Order.objects.filter(billing_email=billing_email).order_by('-date')[0],
        'total' : Order.objects.filter(billing_email=billing_email).aggregate(tot_cnt=Count('order_id'), tot_itm=Sum('item_qty'), tot_spt=Sum('total_price_inc_vat')),  
        'customer' : customer,
        #'annual_summary' : qs,
      }

    return render(request, 'customer-view.html', context )