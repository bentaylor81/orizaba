from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Subquery, OuterRef, DecimalField, IntegerField, Sum, Count
from app_products.models import *
from app_orders.models import *
from app_utils.models import *
from .filters import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from app_users.decorators import unauthenticated_user, allowed_users
from django.core.paginator import Paginator
from django.contrib import messages
from django.views.generic import View, ListView, DetailView, UpdateView
from django_filters.views import FilterView
from django.views.generic.edit import FormMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views import View
from django.forms import formset_factory
from .forms import *
from datetime import datetime  
import requests
import json
import pdfkit
import wkhtmltopdf

class ProductList(LoginRequiredMixin, FilterView):
    login_url = '/login/'
    template_name = 'app_products/product_list/product-list.html'
    model = Product
    paginate_by = 20
    filterset_class = ProductFilter
    strict = False
    form_class = ProductLabelForm

    def post(self, request, *args, **kwargs):
        form = ProductLabelForm(request.POST)
        sku = form.data['sku']
        qty = form.data['qty']
        path = form.data['path']        
        wkhtmltopdf_config = settings.WKHTMLTOPDF_CMD
        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_config)
        options = {'copies' : '1', 'page-width' : '51mm', 'page-height' : '102mm', 'orientation' : 'Landscape', 'margin-top': '0', 'margin-right': '0', 'margin-bottom': '0', 'margin-left': '0', }
        # GENERATE A PDF FILE IN STATIC
        projectUrl = 'http://' + request.get_host() + '/product/label/%s' % sku
        pdf = pdfkit.from_url(projectUrl, "static/pdf/product-label.pdf", configuration=config, options=options)   
        # SELECT THE PRINTER
        process = PrintProcess.objects.get(process_id=3)
        printer_id = process.process_printer.printnode_id     
        # SEND TO PRINTNODE
        payload = '{"printerId": '+str(printer_id)+', "title": "Label for: ' +str(sku)+ ' ", "contentType": "pdf_uri", "content":"https://orizaba.herokuapp.com/static/pdf/product-label.pdf", "source": "GTS Product Label", "options": {"copies": ' +str(qty)+ '}}'
        response = requests.request("POST", "https://api.printnode.com/printjobs", headers=settings.PRINTNODE_HEADERS, data=payload)
        print(response.text.encode('utf8'))
        messages.success(self.request, 'Processing Product Label')
        return HttpResponseRedirect(path)

class ProductDetail(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    template_name = 'app_products/product_detail/product-detail.html'
    form_class = ProductDetailForm
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stock_movement'] = StockMovement.objects.filter(product_id__product_id=self.object.pk)
        context['previous_orders'] = OrderItem.objects.filter(product_id__product_id=self.object.pk)
        context['purchase_order_item'] = PurchaseOrderItem.objects.filter(product__product_id=self.object.pk)
        context['parts_outstanding'] = context['purchase_order_item'].aggregate(Sum('outstanding_qty'))['outstanding_qty__sum'] or 0
        return context

    def get_success_url(self):
        messages.success(self.request, 'Product Updated')
        return reverse('product-detail', kwargs={'pk': self.object.pk})     

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()   
        # STOCK MOVEMENT - ADD A ROW TO THE STOCK MOVEMENT TABLE    
        form = ManualStockAdjustForm(self.request.POST)
        adjustment_qty = form['adjustment_qty'].value()
        if form.is_valid():  
            # Save the form but don't commit
            event = form.save(commit=False)
            # Update the current_stock_qty from the orizaba_stock_qty in the product table
            current_stock_qty = self.object.orizaba_stock_qty + int(adjustment_qty)
            event.current_stock_qty = current_stock_qty
            event.save()
            # Sets the stock value in the product table
            Product.objects.filter(pk=self.object.product_id).update(orizaba_stock_qty=current_stock_qty) 
            messages.success(request, 'Manual Stock Adjustment Added')
            return HttpResponseRedirect(reverse('product-detail', kwargs={'pk': self.object.pk})) 

class PurchaseOrderList(LoginRequiredMixin, FormMixin, FilterView):
    login_url = '/login/'
    template_name = 'app_products/purchase_order_list/purchase-order-list.html'
    model = PurchaseOrder
    paginate_by = 20
    filterset_class = PurchaseOrderFilter
    form_class = PurchaseOrderCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['suppliers'] = Supplier.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form = PurchaseOrderCreateForm(self.request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Purchase Order has been Added')
            return redirect('purchase-order-list')

class PurchaseOrderDetail(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    template_name = 'app_products/purchase_order_detail/purchase-order-detail.html'
    model = PurchaseOrder
    form_class = PurchaseOrderForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        po_item_form = PoItemFormset(instance=self.object)
        return self.render_to_response(self.get_context_data(form=form, po_item_form=po_item_form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['suppliers'] = Supplier.objects.all()
        po_item = PurchaseOrderItem.objects.filter(purchaseorder__po_id=self.object.pk)
        context['total_lines'] = po_item.count or 0 
        context['parts_ordered'] = po_item.aggregate(Sum('order_qty'))['order_qty__sum'] or 0
        context['parts_received'] = po_item.aggregate(Sum('received_qty'))['received_qty__sum'] or 0
        context['parts_outstanding'] = context['parts_ordered'] - context['parts_received'] or 0
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object() 
        po_id = self.object.po_id

        if 'status' in request.POST or 'notes' in request.POST or 'edit-po' in request.POST:
            form = PurchaseOrderForm(self.request.POST, instance=self.object)  
            if form.is_valid(): 
                form.save()
                messages.success(request, 'Purchase Order Saved')
                return HttpResponseRedirect(self.get_success_url())
            else:
                return self.form_invalid(form)
        else:
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            po_item_form = PoItemFormset(self.request.POST, instance=self.object)
            if (po_item_form.is_valid() and form.is_valid()):
                po_item_form.save()
                for form in po_item_form:
                    sku = form['product_sku'].value()
                    qty = form['delivery_qty'].value()  
                    product_id = int(form['product'].value())  
                    comments = form['comments'].value()
                    now = datetime.now()     
                    # STOCK MOVEMENT - ADD A ROW TO THE STOCK MOVEMENT TABLE    
                    if (qty and int(qty) != 0):
                        product_inst = Product.objects.get(pk=product_id)
                        # Adds the current stock qty (Product table) to purchase order qty
                        current_stock_qty = int(product_inst.orizaba_stock_qty) + int(qty) 
                        # Sets the rolling stock value in the Stock Movement row
                        StockMovement.objects.create(date_added=now, product_id=product_inst, adjustment_qty=qty, movement_type="Purchase Order Receipt", purchaseorder_id=po_id, current_stock_qty=current_stock_qty, comments=comments) 
                        # Sets the stock value in the product table
                        Product.objects.filter(pk=product_id).update(orizaba_stock_qty=current_stock_qty)   
                    # PRODUCT LABEL - GENERATE LABEL BASED ON THE CHECKBOX
                    if (form['label'].value()==True):
                        # GENERATE A PDF FILE IN STATIC
                        projectUrl = 'http://' + request.get_host() + '/product/label/%s' % sku
                        pdfkit.from_url(projectUrl, "static/pdf/product-label.pdf", configuration=settings.WKHTMLTOPDF_CONFIG, options=settings.WKHTMLTOPDF_OPTIONS)        
                        # SELECT THE PRINTER
                        process = PrintProcess.objects.get(process_id=3)
                        printer_id = process.process_printer.printnode_id
                        # SEND TO PRINTNODE
                        payload = '{"printerId": '+str(printer_id)+', "title": "Label for: ' +str(sku)+ ' ", "contentType": "pdf_uri", "content":"https://orizaba.herokuapp.com/static/pdf/product-label.pdf", "source": "GTS Product Label", "options": {"copies": ' +str(qty)+ '}}'
                        response = requests.request("POST", "https://api.printnode.com/printjobs", headers=settings.PRINTNODE_HEADERS, data=payload)
                        print(response.text.encode('utf8'))
                return HttpResponseRedirect(self.get_success_url())
            else:
                return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('purchase-order-detail', kwargs={'pk': self.object.pk})   

class Unleashed(LoginRequiredMixin, FilterView):
    login_url = '/login/'
    template_name = 'app_products/unleashed.html'
    queryset = StockMovement.objects.filter(movement_type='Purchase Order Receipt')
    paginate_by = 50
    ordering = ['unleashed_status', '-date_added']
    filterset_class = UnleashedFilter

    def post(self, request, *args, **kwargs):
        id = request.POST.get('id')
        instance = StockMovement.objects.get(id=id)
        form = UnleashedForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
        return redirect('/unleashed')     

class SupplierList(LoginRequiredMixin, ListView):
    login_url = '/login/'
    template_name = 'app_products/supplier-list.html'
    model = Supplier

class BrandList(LoginRequiredMixin, ListView):
    login_url = '/login/'
    template_name = 'app_products/brand-list.html'
    model = Brand

class CustomerList(LoginRequiredMixin, ListView):
    login_url = '/login/'
    template_name = 'app_products/customer-list.html'
    model = Customer

# This Function creates the file which renders the PDF
def generate_label(request, id):
    context = { 
            'product': Product.objects.get(sku=id),
        }
    return render(request, 'app_products/product_list/pdfs/label-create.html', context )




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

    return render(request, 'app_products/supplier-detail.html', context )



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

    return render(request, 'app_products/customer-detail.html', context )