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
from django.utils import timezone
import datetime
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
        # PURCHASE ORDER ITEMS IN STOCK-STATUS.HTML
        purchase_order_item = PurchaseOrderItem.objects.filter(product__product_id=self.object.pk)
        context['parts_outstanding'] = purchase_order_item.aggregate(Sum('outstanding_qty'))['outstanding_qty__sum'] or 0
        context['parts_outstanding_po'] = purchase_order_item.values('purchaseorder', 'purchaseorder__reference', 'purchaseorder__date_ordered').annotate(outstanding=Sum('outstanding_qty')).order_by('-purchaseorder')
        return context

    def get_success_url(self):
        messages.success(self.request, 'Product Updated')
        return reverse('product-detail', kwargs={'pk': self.object.pk})     

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()   
        if 'product-details' in request.POST:
            form = ProductDetailForm(self.request.POST, request.FILES or None, instance=self.object)  
            if form.is_valid(): 
                print(form)
                form.save()
                return HttpResponseRedirect(self.get_success_url())
            else:
                return self.form_invalid(form)

        if 'stock-movement' in request.POST:
            # STOCK MOVEMENT - ADD A ROW TO THE STOCK MOVEMENT TABLE    
            form = ManualStockAdjustForm(self.request.POST)
            adjustment_qty = form['adjustment_qty'].value()
            if form.is_valid():  
                # SAVE THE FORM BUT DON'T COMMIT
                event = form.save(commit=False)
                # UPDATE THE CURRENT_STOCK_QTY FROM THE ORIZABA_STOCK_QTY IN THE PRODUCT TABLE
                current_stock_qty = self.object.orizaba_stock_qty + int(adjustment_qty)
                event.current_stock_qty = current_stock_qty
                event.save()
                # SETS THE STOCK VALUE IN THE PRODUCT TABLE
                Product.objects.filter(pk=self.object.product_id).update(orizaba_stock_qty=current_stock_qty) 
                messages.success(request, 'Manual Stock Adjustment Added')
                return HttpResponseRedirect(reverse('product-detail', kwargs={'pk': self.object.pk})) 
        
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

        if 'status' in request.POST or 'notes' in request.POST or 'edit-po' in request.POST:
            form = PurchaseOrderForm(self.request.POST, instance=self.object)  
            if form.is_valid(): 
                form.save()
                messages.success(request, 'Purchase Order Saved')
                return HttpResponseRedirect(self.get_success_url())
            else:
                return self.form_invalid(form)
        elif 'add-part' in request.POST:
            # GET FORM ATTRIBUTES
            product_id = request.POST.get('product_id')
            order_qty = request.POST.get('order_qty')
            # ADD PART ROW TO THE TABLE
            PurchaseOrderItem.objects.create(product_id=product_id, order_qty=order_qty, outstanding_qty=order_qty, purchaseorder_id=po_id)
            return HttpResponseRedirect(self.get_success_url())
        elif 'reset_part' in request.POST:
            reset_part = request.POST.getlist('reset_part')
            product_id = request.POST.getlist('product_id')
            now = datetime.datetime.now(tz=timezone.utc)
            # UPDATE THE RECEIVED AND OUTSTANDING QTY
            for reset_part, product_id in zip(reset_part, product_id):
                part = PurchaseOrderItem.objects.get(id=reset_part)
                # STOCKMOVEMENT TABLE - REMOVE DELIVERY QTY TO STOCK QTY IN PRODUCT TABLE AND ADD A NEW ROW
                product_inst = Product.objects.get(pk=product_id)
                current_stock_qty = int(product_inst.orizaba_stock_qty) - int(part.received_qty) 
                StockMovement.objects.create(date_added=now, product_id=product_inst, adjustment_qty=-part.received_qty, movement_type="Purchase Order Receipt - Reversal", purchaseorder_id=po_id, current_stock_qty=current_stock_qty) 
                # PRODUCT TABLE - UPDATE THE STOCK VALUE
                Product.objects.filter(pk=product_id).update(orizaba_stock_qty=current_stock_qty)  
                # PURCHASEORDERITEM TABLE - RESET THE RECEIVED QTY
                part.received_qty=0
                part.outstanding_qty=part.order_qty
                part.received_status='Order Pending'
                part.save() 
            return HttpResponseRedirect(self.get_success_url())
        elif 'delete_part' in request.POST:
            delete_part = request.POST.getlist('delete_part')
            # DELETE THE ROW IN PURCHASEORDERITEM
            for delete_part in delete_part:
                PurchaseOrderItem.objects.get(id=delete_part).delete()
            return HttpResponseRedirect(self.get_success_url())
        else:
            # GET LIST OF FORM ATTRIBUTES
            poitem_id = request.POST.getlist('poitem_id')
            product_id = request.POST.getlist('product_id')
            delivery_qty = request.POST.getlist('delivery_qty')
            comments = request.POST.getlist('comments')
            print_label = request.POST.getlist('print_label')
            now = datetime.datetime.now(tz=timezone.utc)
            count = 0
            # ITERATE OVER THE FORM LISTS
            for poitem_id, product_id, delivery_qty, comments, print_label in zip(poitem_id, product_id, delivery_qty, comments, print_label):
                # CALCULATE OUTSTANDING AND RECEIVED QUANTITES
                item = PurchaseOrderItem.objects.get(id=poitem_id)
                received_qty = item.received_qty + int(delivery_qty)
                outstanding_qty = item.order_qty - received_qty
                # SET THE STATUS BASED ON THE OUTSTANDING QUANTITY
                if(outstanding_qty == 0):
                    received_status = 'Full Receipt'
                elif(outstanding_qty != 0 and outstanding_qty < item.order_qty):
                    received_status = 'Partial Receipt'
                else:
                    received_status = 'Order Pending'
                # UPDATE THE COMMENTS FIELD IN PURCHASEORDERITEM
                if(comments != item.comments):
                    PurchaseOrderItem.objects.filter(id=poitem_id).update(comments=comments)                
                # UPDATE THE TABLES FOR EACH ITEM
                if(int(delivery_qty) > 0):  
                    # PURCHASEORDERITEM - UPDATE ROW FOR POITEM_ID
                    PurchaseOrderItem.objects.filter(id=poitem_id).update(product_id=product_id, received_qty=received_qty, outstanding_qty=outstanding_qty, received_status=received_status, date_updated=now)
                    # STOCKMOVEMENT TABLE - ADD DELIVERY QTY TO STOCK QTY IN PRODUCT TABLE AND ADD A NEW ROW   
                    product_inst = Product.objects.get(pk=product_id)
                    current_stock_qty = int(product_inst.orizaba_stock_qty) + int(delivery_qty) 
                    StockMovement.objects.create(date_added=now, product_id=product_inst, adjustment_qty=delivery_qty, movement_type="Purchase Order Receipt", purchaseorder_id=po_id, current_stock_qty=current_stock_qty) 
                    # PRODUCT TABLE - UPDATE THE STOCK VALUE
                    Product.objects.filter(pk=product_id).update(orizaba_stock_qty=current_stock_qty)   
                    # PRODUCT LABEL - GENERATE LABEL BASED ON THE LABEL CHECKBOX
                    if(print_label == 'true'):
                        # GENERATE A PDF FILE IN STATIC
                        projectUrl = 'http://' + request.get_host() + '/product/label/%s' % product_inst.sku
                        pdfkit.from_url(projectUrl, "static/pdf/product-label.pdf", configuration=settings.WKHTMLTOPDF_CONFIG, options=settings.WKHTMLTOPDF_OPTIONS)        
                        # SELECT THE PRINTER
                        process = PrintProcess.objects.get(process_id=3)
                        printer_id = process.process_printer.printnode_id
                        # SEND TO PRINTNODE
                        payload = '{"printerId": '+str(printer_id)+', "title": "Label for: ' +str(product_inst.sku)+ ' ", "contentType": "pdf_uri", "content":"https://orizaba.herokuapp.com/static/pdf/product-label.pdf", "source": "GTS Product Label", "options": {"copies": ' +str(delivery_qty)+ '}}'
                        response = requests.request("POST", "https://api.printnode.com/printjobs", headers=settings.PRINTNODE_HEADERS, data=payload)
                        print(response.text.encode('utf8'))
            
            return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('purchase-order-detail', kwargs={'pk': self.object.pk})   

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