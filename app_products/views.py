from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Subquery, OuterRef, DecimalField, IntegerField, Sum, Count
from app_products.models import *
from app_orders.models import *
from app_utils.models import *
from app_products.utils import *
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
from datetime import datetime, date  
from django.utils import timezone
import datetime
import requests
import json
import pdfkit
import wkhtmltopdf
import time

class ProductList(LoginRequiredMixin, FilterView):
    login_url = '/login/'
    template_name = 'app_products/product_list/product-list.html'
    model = Product
    paginate_by = 10
    filterset_class = ProductFilter
    strict = False
    form_class = ProductLabelForm

    def post(self, request, *args, **kwargs):
        # PRINT PRODUCT LABEL
        form = ProductLabelForm(request.POST)
        form.save()
        # RUN PRINT LABEL FUNCTION FROM UTILS.PY
        printProductLabel(request)
        messages.success(self.request, 'Processing Product Label')
        return HttpResponseRedirect(reverse('product-list'))

class ProductDetail(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    template_name = 'app_products/product_detail/product-detail.html'
    form_class = ProductDetailForm
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['suppliers'] = Supplier.objects.all()
        context['brands'] = Brand.objects.all()
        context['stock_movement'] = StockMovement.objects.filter(product=self.object)
        context['previous_orders'] = OrderItem.objects.filter(product_id=self.object)
        # PURCHASE ORDER ITEMS IN STOCK-STATUS.HTML
        purchase_order_item = PurchaseOrderItem.objects.filter(product=self.object)
        context['parts_outstanding'] = purchase_order_item.aggregate(Sum('outstanding_qty'))['outstanding_qty__sum'] or 0
        context['parts_outstanding_po'] = purchase_order_item.values('purchaseorder', 'purchaseorder__reference', 'purchaseorder__date_ordered').annotate(outstanding=Sum('outstanding_qty')).order_by('-purchaseorder')
        # STOCK LOCATION HISTORY
        context['stock_location'] = StockLocation.objects.filter(product=self.object)
        # STOCK CHECK 
        context['stock_check'] = StockCheck.objects.filter(product=self.object)
        return context

    def get_success_url(self):
        messages.success(self.request, 'Product Updated')
        return reverse('product-detail', kwargs={'pk': self.object.pk})     

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()   
        now = datetime.datetime.now(tz=timezone.utc)
        if 'product-details' in request.POST:
            form = ProductDetailForm(self.request.POST, request.FILES or None, instance=self.object)  
            if form.is_valid(): 
                form.save()
                return HttpResponseRedirect(self.get_success_url())
            else:
                return self.form_invalid(form)

        elif 'stock-movement' in request.POST:
            # STOCK MOVEMENT - ADD A ROW TO THE STOCK MOVEMENT TABLE    
            form = ManualStockAdjustForm(self.request.POST)
            adjustment_qty = form['adjustment_qty'].value()
            if form.is_valid():  
                # SAVE THE FORM BUT DON'T COMMIT
                event = form.save(commit=False)
                # STOCK MOVEMENT TABLE - ADD A NEW MOVEMENT ROW
                new_stock_qty = self.object.orizaba_stock_qty + int(adjustment_qty)
                event.current_stock_qty = new_stock_qty
                event.date_added = now
                event.save()
                # PRODUCT TABLE - SETS THE STOCK QTY 
                self.object.orizaba_stock_qty = new_stock_qty
                self.object.save()
                # MAGENTO SYNC TABLE - CREATE A ROW AND RUN FUNCTION
                MagentoProductSync.objects.create(product=self.object, stock_qty=self.object.orizaba_stock_qty)
                magento_sync(request)
                
                messages.success(request, 'Manual Stock Adjustment Added')
                return HttpResponseRedirect(reverse('product-detail', kwargs={'pk': self.object.pk})) 

        elif 'edit-location' in request.POST: 
            location = request.POST.get('location')
            # CREATE ROW IN STOCK LOCATION TABLE
            StockLocation.objects.create(product=self.object, location=location)
            # UPDATE ROW IN PRODUCT TABLE
            self.object.location = location
            self.object.save()
            return HttpResponseRedirect(self.get_success_url())  

        elif 'stock-check' in request.POST: 
            actual_qty = request.POST.get('actual_qty')
            difference_qty = request.POST.get('difference_qty')
            # STOCKCHECK TABLE - CREATE A ROW FOR THE STOCK CHECK
            StockCheck.objects.create(product=self.object, expected_qty=self.object.orizaba_stock_qty, actual_qty=actual_qty, difference_qty=difference_qty)
            # STOCK MOVEMENT TABLE - CREATE A ROW
            StockMovement.objects.create(product=self.object, date_added=now, adjustment_qty=difference_qty, movement_type="Stock Check", current_stock_qty=actual_qty)    
            # PRODUCT TABLE - UPDATE STOCK_QTY
            self.object.orizaba_stock_qty = actual_qty
            self.object.last_stock_check = now
            self.object.save()
            # MAGENTO SYNC TABLE - CREATE A ROW AND RUN FUNCTION
            MagentoProductSync.objects.create(product=self.object, stock_qty=self.object.orizaba_stock_qty)
            magento_sync(request)

            messages.success(request, 'Stock Check Added')  
        
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # EDIT DETAILS MODAL
        context['suppliers'] = Supplier.objects.all()
        # PURCHASE ORDER DETAILS
        po_item = PurchaseOrderItem.objects.filter(purchaseorder__po_id=self.object.pk)
        # SET THE TOTALS
        self.object.total_lines = po_item.count() or 0
        self.object.order_qty = po_item.aggregate(Sum('order_qty'))['order_qty__sum'] or 0
        self.object.received_qty = po_item.aggregate(Sum('received_qty'))['received_qty__sum'] or 0
        self.object.outstanding_qty = po_item.aggregate(Sum('outstanding_qty'))['outstanding_qty__sum'] or 0
        # SET THE STATUS
        if(self.object.outstanding_qty == 0 ):
            self.object.status = 'Complete'
        elif(self.object.received_qty == 0 ):
            self.object.status = 'Pending'
        else:
            self.object.status = 'Part Receipt'
        self.object.save()
        # PURCHASE ORDER ITEMS
        context['po_items'] = PurchaseOrderItem.objects.filter(purchaseorder__po_id=self.object.pk)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object() 
        po_id = self.object.po_id
        now = datetime.datetime.now(tz=timezone.utc)

        if 'status' in request.POST or 'notes' in request.POST or 'edit-po' in request.POST:
            form = PurchaseOrderForm(self.request.POST, instance=self.object)  
            if form.is_valid(): 
                form.save()
                messages.success(request, 'Purchase Order Saved')
                return HttpResponseRedirect(self.get_success_url())
            else:
                return self.form_invalid(form)

        elif 'add-part' in request.POST:
            product_id = request.POST.get('product_id')
            order_qty = request.POST.get('order_qty')
            # ADD PART ROW TO THE TABLE
            PurchaseOrderItem.objects.create(product_id=product_id, order_qty=order_qty, outstanding_qty=order_qty, purchaseorder_id=po_id)
            return HttpResponseRedirect(self.get_success_url())

        elif 'reset_part' in request.POST:
            reset_part = request.POST.get('reset_part')
            po_item = PurchaseOrderItem.objects.get(id=reset_part)
            # STOCKMOVEMENT TABLE - REMOVE DELIVERY QTY TO STOCK QTY IN PRODUCT TABLE AND ADD A NEW ROW
            new_stock_qty = int(po_item.product.orizaba_stock_qty) - int(po_item.received_qty) 
            StockMovement.objects.create(date_added=now, product=po_item.product, adjustment_qty=-po_item.received_qty, movement_type="Purchase Order Receipt - Reversal", purchaseorder_id=po_id, current_stock_qty=new_stock_qty) 
            # MAGENTO SYNC TABLE - CREATE A ROW AND RUN FUNCTION
            MagentoProductSync.objects.create(product=po_item.product, stock_qty=new_stock_qty) 
            magento_sync(request)
            # PRODUCT TABLE - UPDATE STOCK QTY
            po_item.product.orizaba_stock_qty = new_stock_qty
            po_item.product.save()
            # PURCHASEORDERITEM TABLE - RESET THE RECEIVED QTY
            po_item.received_qty = 0
            po_item.outstanding_qty=po_item.order_qty
            po_item.received_status='Order Pending'
            po_item.save() 
            return HttpResponseRedirect(self.get_success_url())

        elif 'delete_part' in request.POST:
            delete_part = request.POST.get('delete_part')
            # DELETE THE ROW IN PURCHASEORDERITEM
            PurchaseOrderItem.objects.get(id=delete_part).delete()
            return HttpResponseRedirect(self.get_success_url())

        else:
            # GET LIST OF FORM ATTRIBUTES
            poitem_id = request.POST.getlist('poitem_id')
            delivery_qty = request.POST.getlist('delivery_qty')
            comments = request.POST.getlist('comments')
            print_label = request.POST.getlist('print_label')
            # ITERATE OVER THE FORM LISTS
            for poitem_id, delivery_qty, comments, print_label in zip(poitem_id, delivery_qty, comments, print_label):
                # CALCULATE OUTSTANDING AND RECEIVED QUANTITES
                poitem = PurchaseOrderItem.objects.get(id=poitem_id)
                received_qty = poitem.received_qty + int(delivery_qty)
                outstanding_qty = poitem.order_qty - received_qty
                # SET THE STATUS BASED ON THE OUTSTANDING QUANTITY
                if(outstanding_qty == 0):
                    received_status = 'Full Receipt'
                elif(outstanding_qty != 0 and outstanding_qty < poitem.order_qty):
                    received_status = 'Partial Receipt'
                else:
                    received_status = 'Order Pending'
                # PURCHASEORDERITEM - UPDATE THE COMMENTS FIELD
                if(comments != poitem.comments):
                    poitem.comments = comments
                    poitem.save()             
                # UPDATE THE TABLES FOR EACH ITEM
                if(int(delivery_qty) > 0):  
                    # PURCHASEORDERITEM - UPDATE ROW FOR POITEM_ID
                    poitem.received_qty = received_qty
                    poitem.outstanding_qty = outstanding_qty
                    poitem.received_status = received_status
                    poitem.date_updated = now
                    poitem.save()
                    # STOCKMOVEMENT TABLE - ADD DELIVERY QTY TO STOCK QTY IN PRODUCT TABLE AND ADD A NEW ROW   
                    new_stock_qty = int(poitem.product.orizaba_stock_qty) + int(delivery_qty) 
                    StockMovement.objects.create(date_added=now, product=poitem.product, adjustment_qty=delivery_qty, movement_type="Purchase Order Receipt", purchaseorder_id=po_id, current_stock_qty=new_stock_qty) 
                    # PRODUCT TABLE - UPDATE STOCK QTY
                    poitem.product.orizaba_stock_qty = new_stock_qty
                    poitem.product.save()
                    # MAGENTO SYNC TABLE - CREATE A ROW AND RUN FUNCTION
                    MagentoProductSync.objects.create(product=poitem.product, stock_qty=new_stock_qty)
                    magento_sync(request)
                    # PRODUCT LABEL - GENERATE LABEL BASED ON THE LABEL CHECKBOX
                    if(print_label == 'true'):
                        # PRODUCTLABE - CREATE A NEW ROW
                        ProductLabel.objects.create(product=poitem.product, qty=delivery_qty)
                        # RUN PRINT LABEL FUNCTION FROM UTILS.PY
                        printProductLabel(request)

            return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('purchase-order-detail', kwargs={'pk': self.object.pk})   

class StockCheckList(LoginRequiredMixin, ListView):
    login_url = '/login/'
    template_name = 'app_products/stock-check-list.html'
    model = StockCheck
    paginate_by = 20

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

# PRODUCT LABEL - CREATE THE FILE WHICH RENDERS THE PDF LABEL
def generate_label(request, id):
    context = { 
            'product': Product.objects.get(product_id=id),
        }
    return render(request, 'app_products/product_list/pdfs/label-create.html', context )

# MAGENTO STOCK SYNC - UPDATE THE STOCK VALUE IN MAGENTO 
def magento_sync(request): 
    now = datetime.datetime.now(tz=timezone.utc)
    sync_products = MagentoProductSync.objects.filter(has_synced=False).order_by('id')
    # LOOP TO POST TO MAGENTO
    for product in sync_products:
        payload='{"product_id":"'+str(product.product_id)+'","stock_qty":"'+str(product.stock_qty)+'"}'
        response = requests.request("POST", settings.MAGENTO_URL, headers=settings.MAGENTO_HEADERS, data=payload)
        # MAGENTOPRODUCTSYNC - UPDATE HAS_SYNCED TO TRUE AND DATE_SYNCED
        has_updated = json.loads(response.text)['updated']
        if has_updated == True:
            product.has_synced = True
            product.date_synced = now
            product.save()
        print(response.text)
        # APILOG - ADD ROW    
        ApiLog.objects.create(process='Sync Products', api_service='Magento', response_code=response, response_text=response.text)   





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