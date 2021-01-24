from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Subquery, OuterRef, DecimalField, IntegerField, Sum, Count
from app_products.models import *
from app_utils.models import *
from .filters import *
from django.contrib.auth.decorators import login_required
from app_users.decorators import unauthenticated_user, allowed_users
from django.core.paginator import Paginator
from .forms import *
from .utils import *
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView, DetailView, FormView, UpdateView
from django.views.generic.edit import FormMixin, CreateView
from django_filters.views import FilterView
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
import datetime
import requests
import json
import pdfkit
import wkhtmltopdf
from django_q.tasks import async_task
import rollbar
from django.core import serializers

class OrderList(LoginRequiredMixin, FilterView):
    login_url = '/login/'
    template_name = 'app_orders/order_list/order-list.html'
    model = Order
    paginate_by = 20
    filterset_class = OrderFilter
    strict = False
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_path'] = self.request.get_full_path()
        return context

class OrderDetail(LoginRequiredMixin, FormMixin, DetailView):
    login_url = '/login/'
    template_name = 'app_orders/order_detail/order-detail.html'
    queryset = Order.objects.all()
    form_class = OrderShipmentForm
    model = Order

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        order_id = self.object.order_id
        context = super().get_context_data(**kwargs)  
        context['delivery_methods'] = OrderDeliveryMethod.objects.all()
        context['order_items'] = OrderItem.objects.filter(order_id=order_id)
        context['order_status_type'] = OrderStatusType.objects.all()
        context['refunds'] = RefundOrder.objects.filter(order_id=order_id)
        context['postage_already_refunded'] = RefundOrderItem.objects.filter(Q(order_id=order_id) & Q(refund_type='Postage Refund')).exists()
        context['manual_refund_processed'] = RefundOrderItem.objects.filter(Q(order_id=order_id) & Q(refund_type='Manual Refund Amount')).exists()
        return context

    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Order, order_id=id_)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        order_id = self.object.order_id
        order_no = self.object.order_no
        form_order_id = Order.objects.get(pk=order_id)
        
        if 'print-picklist' in request.POST:
            # UPDATED WITHOUT USING A FORM IN FORMS.PY
            orderitem = request.POST.getlist('orderitem_id')
            send_qty = request.POST.getlist('send_qty')
            # UPDATE THE SEND QTY IN THE PICKLIST
            for oi, sq in [(orderitem, send_qty)]:
                i=0
                while (i < len(oi)):
                    instance = OrderItem.objects.get(orderitem_id=oi[i])
                    instance.send_qty = sq[i]
                    instance.save()
                    i+=1
            # PASS THE SEND QTY INTO THE PDF GENERATOR
            self.print_picklist(self.request)   
            messages.success(self.request, 'Picklist is Printing') 

        elif 'add-shipment' in request.POST:  
            form_class = self.get_form_class()
            form = self.get_form(form_class)                   
            # COUNT THE NUMBER OF SHIPMENTS AND CONCATENATE TO ORDER_NO, TO AVOID DUPLICATING REF
            shipment_no = OrderShipment.objects.filter(order_id=order_id).count()
            global shipping_ref
            if shipment_no != 0:
                shipping_ref = str(order_no) + '/' + str(shipment_no)
            else: 
                shipping_ref = str(order_no)
            # SUBMIT THE FORM
            if form.is_valid():
                form.instance.order_id = form_order_id
                form.instance.shipping_ref = shipping_ref
                form.save()          
                # UPDATE THE SEND QTY FOR THE PICKLIST
                orderitem = request.POST.getlist('orderitem_id')
                send_qty = request.POST.getlist('send_qty')
                for oi, sq in [(orderitem, send_qty)]:
                    i=0
                    while (i < len(oi)):
                        instance = OrderItem.objects.get(orderitem_id=oi[i])
                        instance.send_qty = sq[i]
                        instance.save()
                        i+=1
                # PRINT THE PICKLIST IF PICKLIST CHECKBOX IS TRUE
                picklist = form['picklist'].value()
                if picklist == True:
                    self.print_picklist(self.request)  
                # ADD THE SHIPMENT CREATED AND PICKLIST PRINTED STATUS TO ORDER STATUS HISTORY TABLE
                now = datetime.datetime.now()
                order_inst = Order.objects.get(order_id=order_id)
                type_inst = OrderStatusType.objects.get(pk=20)
                OrderStatusHistory.objects.create(order_id=order_inst, status_type=type_inst, date=now)
                # SET THE STATUS IN THE ORDER TABLE TO SHIPMENT CREATED
                order_inst.status_current = type_inst
                order_inst.save()  
                # CREATE SHIPTHEORY SHIPMENT METHOD
                shipment = OrderShipment.objects.get(shipping_ref=shipping_ref)
                service_id = shipment.service_id.service_id 
                firstname = shipment.delivery_firstname
                lastname = shipment.delivery_lastname
                address_1 = shipment.delivery_address_1
                address_2 = shipment.delivery_address_2
                city = shipment.delivery_city
                postcode = shipment.delivery_postcode
                country = shipment.delivery_country_code
                phone = shipment.delivery_phone
                email = shipment.delivery_email
                total_price = shipment.total_price_ex_vat
                weight = shipment.weight
                # GET PRODUCT INFORMATION
                shipment_products = OrderItem.objects.filter(order_id=order_inst)
                product_lines = []
                for product in shipment_products:
                    if product.send_qty > 0:
                        product_price = product.send_qty * product.item_price
                        line = {'sku': str(product.product_id.sku),"name": str(product.product_id.product_name),"value":float(product_price),"weight":float(product.product_id.weight),"commodity_code":"84329000","commodity_description":"Parts for Garden Machinery","commodity_manucountry":"GB","commodity_composition":"Metal and Plastic"}
                        product_lines.append(line)
                product_lines = json.dumps(product_lines)
                # CREATE SHIPTHEORY SHIPMENT
                payload = '{"reference":"'+str(shipping_ref)+'","reference2":"GTS","delivery_service":"'+str(service_id)+'","increment":"1","shipment_detail":{"weight":"'+str(weight)+'","parcels":1,"value":'+str(total_price)+'},"recipient":{"firstname":"'+firstname+'","lastname":"'+lastname+'","address_line_1":"'+address_1+'","address_line_2":"'+address_2+'","city":"'+city+'","postcode":"'+postcode+'","country":"'+country+'","telephone":"'+phone+'","email":"'+email+'"},"products":'+str(product_lines)+'}'
                response = requests.request("POST", "https://api.shiptheory.com/v1/shipments", headers=settings.ST_HEADERS, data=payload)
                print(payload)
                print(response.text)
                ApiLog.objects.create(process='Create Shipment', api_service='Ship Theory', response_code=response, response_text=response.text) # LOG RESULT  
                # GET THE TRACKING CODE FROM RESULT AND SAVE
                tracking_code = (json.loads(response.text)['carrier_result']['tracking'])
                if tracking_code:
                    shipment.tracking_code = tracking_code
                    shipment.save() 
                messages.success(self.request, 'Shipment Created and Label Processing')  
            else:
                return self.form_invalid(form)

        elif 'add-note' in request.POST:
            form = OrderNoteForm(request.POST or None)
            if form.is_valid(): 
                form.instance.added_by = request.user.first_name
                form.instance.order_id = form_order_id
                form.save()
                messages.success(request, 'Note has been added')
            else:
                return self.form_invalid(form)
        
        elif 'edit-delivery-details' in request.POST: 
            form = OrderDeliveryDetailsForm(self.request.POST, instance=self.object)  
            if form.is_valid():
                form.order_id = form_order_id
                form.save()
                messages.success(self.request, 'Delivery Details Updated')
            else:
                return self.form_invalid(form)

        elif 'download-invoice' in request.POST:
            # GENERATE AND DOWNLOAD PDF
            projectUrl = 'http://' + request.get_host() + '/orders/%s/invoice' % order_id    
            pdf = pdfkit.from_url(projectUrl, False, configuration=settings.WKHTMLTOPDF_CONFIG)
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = "attachment; filename=Invoice-%s.pdf" % order_no
            return response

        elif 'print-invoice' in request.POST:
            # GENERATE PDF
            projectUrl = 'http://' + request.get_host() + '/orders/%s/invoice' % order_id  
            pdfkit.from_url(projectUrl, "static/pdf/invoice.pdf", configuration=settings.WKHTMLTOPDF_CONFIG)
            # SELECT THE PRINTER
            process = PrintProcess.objects.get(process_id=2)
            printer_id = process.process_printer.printnode_id
            # SEND TO PRINTNODE
            payload = '{"printerId": '+str(printer_id)+', "title": "Invoice for: ' +str(order_no)+ ' ", "contentType": "pdf_uri", "content":"https://orizaba.herokuapp.com/static/pdf/invoice.pdf", "source": "GTS Order Invoice"}'
            response = requests.request("POST", "https://api.printnode.com/printjobs", headers=settings.PRINTNODE_HEADERS, data=payload)
            print(response.text.encode('utf8'))
            ApiLog.objects.create(process='Print Invoice', api_service='PrintNode', response_code=response, response_text=response.text) # LOG RESULT  
            messages.success(self.request, 'Printing Invoice')

        elif 'email-invoice' in request.POST:
            # GENERATE PDF
            projectUrl = 'http://' + request.get_host() + '/orders/%s/invoice' % order_id
            pdfkit.from_url(projectUrl, "static/pdf/GTS-Invoice.pdf", configuration=settings.WKHTMLTOPDF_CONFIG)
            # SEND EMAIL VIA MAILGUN
            form = EmailInvoiceForm(self.request.POST)
            to_email = form.data['to_email']
            if form.is_valid():
                data = {'from': settings.MAILGUN_FROM, 'to': to_email, 'bcc': settings.MAILGUN_BCC, 'subject': form.data['subject'], 'html': form.data['message']}
                files = [('attachment', open('static/pdf/GTS-Invoice.pdf','rb'))]
                response = requests.request("POST", settings.MAILGUN_URL, headers=settings.MAILGUN_HEADERS, data=data, files=files)
                print(response.text.encode('utf8'))
                ApiLog.objects.create(process='Email Invoice', api_service='Mailgun', response_code=response, response_text=response.text) # LOG RESULT  
                messages.success(self.request, 'Invoice has been emailed to ' + to_email)
            else: 
                print(form.errors)
                messages.error(self.request, 'Invoice not sent as the form has errors')

        elif 'process-refund' in request.POST:
            form = RefundOrderForm(request.POST or None)   
            if form.is_valid():
                # SET VARIABLES FOR SAGEPAY REFUND, XERO CREDITNOTE AND PDF CREDITNOTE
                order_inst = Order.objects.get(order_id=order_id)     
                ref_count = RefundOrder.objects.filter(order_id=order_id).count()
                billing_name = order_inst.billing_firstname + ' ' + order_inst.billing_lastname
                if ref_count > 0:
                    ref_txcode = 'Refund-' + str(order_no) + '-' + str(ref_count)
                    ref_cn_number = 'CN-' + str(order_no) + '-' + str(ref_count)
                else:
                    ref_txcode = 'Refund-' + str(order_no)
                    ref_cn_number = 'CN-' + str(order_no)
                now = datetime.datetime.now()
                # ADDS A ROW TO THE REFUNDORDER TABLE
                form.instance.order_id = form_order_id
                form.instance.credit_note_number = ref_cn_number
                form.save()
                # ADD ROW TO REFUNDORDERITEM TABLE CORRESPONDING TO REFUNDED ITEMS
                orderitem_id = request.POST.getlist('orderitem_id')
                item_price = request.POST.getlist('item_price')
                item_qty = request.POST.getlist('item_qty')
                refund_type = request.POST.getlist('refund_type')
                line_description = request.POST.getlist('line_description')
                xero_line_item = request.POST.getlist('xero_line_item')
                refundorder_id = RefundOrder.objects.latest('id')
                # ITERATE OVER THE FORM LISTS
                for orderitem_id, item_price, item_qty, refund_type, line_description, xero_line_item in zip(orderitem_id, item_price, item_qty, refund_type, line_description, xero_line_item):
                    if int(item_qty) > 0:
                        total_price = float(item_price) * int(item_qty)
                        # CREATE A ROW IN REFUNDORDERITEM
                        RefundOrderItem.objects.create(
                            refund_type=refund_type,
                            orderitem_id=orderitem_id,
                            order_id=form_order_id,
                            refundorder=refundorder_id,
                            item_price=item_price,
                            item_qty=item_qty,
                            total_price = total_price,
                            line_description = line_description,
                            xero_line_item = xero_line_item
                            )
                        # UPDATE ORDERITEM TABLE WITH THE REFUNDED_QTY
                        try:
                            orderitem_form = OrderItem.objects.get(orderitem_id=orderitem_id)
                            already_refunded_qty = RefundOrderItem.objects.filter(orderitem_id=orderitem_id).aggregate(Sum('item_qty'))['item_qty__sum'] or 0.00    
                            orderitem_form.refunded_qty = already_refunded_qty
                            orderitem_form.save()
                        except:
                            print('Last item not valid')
                # UPDATE ORDER TABLE WITH THE AMOUNT REFUNDED
                order_table = Order.objects.get(order_id=order_id)
                refund_amount = RefundOrder.objects.filter(order_id=order_id).aggregate(Sum('refund_amount'))['refund_amount__sum'] or 0.00
                order_table.amount_refunded = refund_amount
                order_table.save()
                # ADD THE ORDER REFUNDED STATUS TO ORDER STATUS HISTORY TABLE
                type_inst = OrderStatusType.objects.get(pk=80)
                OrderStatusHistory.objects.create(order_id=order_inst, status_type=type_inst, date=now)
                # PROCESS REFUND IN SAGEPAY
                refundorder = RefundOrder.objects.filter(order_id=order_id).order_by('-pk')[0]  
                url = "https://pi-live.sagepay.com/api/v1/transactions"
                refund_amount = int(refundorder.refund_amount * 100)
                sagepay_tx_id = self.object.sagepay_tx_id     
                sagepay_payload = '{"transactionType":"Refund","referenceTransactionId":"'+str(sagepay_tx_id)+'","vendorTxCode":"'+str(ref_txcode)+'","amount":'+str(refund_amount)+',"description":"'+str(refundorder.refund_reason)+'"}'
                response = requests.request("POST", url, headers=settings.SAGEPAY_HEADERS, data=sagepay_payload)
                print(response.text)
                ApiLog.objects.create(process='Process Refund', api_service='Sagepay', response_code=response, response_text=response.text) # LOG RESULT                
                # CREATE A CREDITNOTE IN XERO
                url = "https://api.xero.com/api.xro/2.0/CreditNotes" 
                refundorderitems = RefundOrderItem.objects.filter(refundorder_id=refundorder).order_by('date_time')
                line_items = []
                for item in refundorderitems:
                    line = {"Description": str(item.line_description) , "Quantity": str(item.item_qty) , "UnitAmount": str(item.item_price) , "AccountCode": str(item.xero_line_item) }
                    line_items.append(line)
                xero_payload = '{"Type":"ACCRECCREDIT","Status":"AUTHORISED","Contact":{"Name": "'+str(billing_name)+'"},"CreditNoteNumber":"'+str(ref_cn_number)+'","Reference":"'+str(ref_cn_number)+'","Date":"'+str(now)+'","LineAmountTypes":"Exclusive","LineItems":'+str(line_items)+'}'
                response = requests.request("POST", url, headers=settings.XERO_HEADERS, data=xero_payload)
                print(xero_payload)
                print('############')
                print(response.text)
                ApiLog.objects.create(process='Process Refund', api_service='Xero', response_code=response, response_text=response.text) # LOG RESULT  
                # GENERATE CREDITNOTE PDF
                projectUrl = 'http://' + request.get_host() + '/orders/%s/credit-note' % order_id
                pdfkit.from_url(projectUrl, "static/pdf/credit-notes/%s.pdf" % ref_cn_number, configuration=settings.WKHTMLTOPDF_CONFIG)
                # EMAIL CREDITNOTE TO THE CUSTOMER
                to_email = order_inst.billing_email.billing_email
                attachment = 'static/pdf/credit-notes/%s.pdf' % ref_cn_number
                subject = 'Your Credit Note is Attached'
                html = request.POST.get('email-html')
                data = {'from': settings.MAILGUN_FROM, 'to': to_email, 'bcc': settings.MAILGUN_BCC, 'subject': subject, 'html': html}
                files = [('attachment', open(attachment,'rb'))]
                response = requests.request("POST", settings.MAILGUN_URL, headers=settings.MAILGUN_HEADERS, data=data, files=files)
                print(response.text.encode('utf8'))
                ApiLog.objects.create(process='Process Refund', api_service='Mailgun', response_code=response, response_text=response.text) # LOG RESULT  
                # UPDATE THE STOCK VALUE FOR THE PRODUCTS
                stockitems = RefundOrderItem.objects.filter(refundorder_id=refundorder) 
                for stockitem in stockitems: 
                    if(stockitem.refund_type == 'Order Item Refund'):
                        orderitem_inst = OrderItem.objects.get(orderitem_id=stockitem.orderitem_id)  
                        product_id = orderitem_inst.product_id
                        adjustment_qty = stockitem.item_qty
                        orizaba_stock_qty = orderitem_inst.product_id.orizaba_stock_qty
                        comments = stockitem.refundorder.refund_reason
                        # GETS NEW ROLLING STOCK QTY VALUE IN STOCKMOVEMENT TABLE
                        current_stock_qty = int(orizaba_stock_qty) + int(stockitem.item_qty) 
                        # CREATE ROW IN STOCKMOVEMENT TABLE     
                        StockMovement.objects.create(date_added=now, product_id=product_id, adjustment_qty=adjustment_qty, movement_type="Returned Item", order_id=order_inst, current_stock_qty=current_stock_qty, comments=comments) 
                        # ADDS NEW STOCK QTY TO QTY IN PRODUCT TABLE
                        Product.objects.filter(pk=product_id.pk).update(orizaba_stock_qty=current_stock_qty)            
                messages.success(request, 'Refund has been Processed')
            else:
                return self.form_invalid(form)

        elif 'status_type' in request.POST:
            form = OrderStatusHistoryForm(request.POST or None)
            if form.is_valid():
                new_status = int(request.POST.get('status_type'))
                order_inst = Order.objects.get(order_id=order_id)
                now = datetime.datetime.now()
                # ADD STATUS ENTRY TO ORDERSTATUSHISTORYTABLE
                form.instance.order_id = form_order_id
                form.instance.date = now
                form.save()
                ### UPDATE ORDERS TABLE BASED ON STATUS TYPES
                # MAIN ORDER STATUSES - SET ORDER TABLE STATUS_CURRENT TO NEW STATUS
                if new_status in range(0, 45):
                    type_inst = OrderStatusType.objects.get(pk=new_status) 
                    order_inst.status_current = type_inst
                # RETURN PENDING STATUS - SET RETURN_ORDER FLAG TO TRUE
                elif new_status in range(50, 85):
                    order_inst.return_order = True  
                    # SET THE STATUS FLAGS AND DATES TO SHOW IN THE RETURNS TABLE 
                    if new_status == 60:
                        order_inst.item_received = True
                        order_inst.item_received_date = now   
                    elif new_status == 70:
                        order_inst.inspection_passed = True
                        order_inst.inspection_passed_date = now
                    elif new_status == 80:
                        order_inst.item_refunded = True
                        order_inst.item_refunded_date = now              
                # RETURN CANCELLED STATUS - SET RETURN_ORDER FLAG TO FALSE
                elif new_status == 90:
                    order_inst.return_order = False
      
                order_inst.save()
                messages.success(request, 'Status has been Updated')
            else:
                return self.form_invalid(form)

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('order-detail', kwargs={'pk': self.object.pk})

    def print_picklist(self, request):    
        ### GENERATE THE PDF PICKLIST - UNCOMMENT BELOW IF YOU DON'T WANT TO USE THE TASK ###
        order_id = self.object.order_id
        order_no = self.object.order_no 
        # GENERATE THE PDF
        wkhtmltopdf_config = settings.WKHTMLTOPDF_CMD
        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_config)
        projectUrl = 'http://' + request.get_host() + '/orders/%s/picklist' % order_id
        pdf = pdfkit.from_url(projectUrl, "static/pdf/picklist.pdf", configuration=config)
        # SELECT THE PRINTER
        process = PrintProcess.objects.get(process_id=1)
        printer_id = process.process_printer.printnode_id
        # SEND TO PRINTNODE
        payload = '{"printerId": '+str(printer_id)+', "title": "Picking List for: '+str(order_no)+'", "color": "true", "contentType": "pdf_uri", "content":"https://orizaba.herokuapp.com/static/pdf/picklist.pdf", "source": "GTS Picking List"}'
        response = requests.request("POST", "https://api.printnode.com/printjobs", headers=settings.PRINTNODE_HEADERS, data=payload)
        print(response.text.encode('utf8'))      
        return

class ReturnList(LoginRequiredMixin, FilterView):
    login_url = '/login/'
    template_name = 'app_orders/return_list/return-list.html'
    model = Order
    queryset = Order.objects.filter(return_order=True)
    paginate_by = 20
    filterset_class = ReturnFilter
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_path'] = self.request.get_full_path()
        return context

class RefundList(LoginRequiredMixin, FilterView):
    login_url = '/login/'
    template_name = 'app_orders/refund_list/refund-list.html'
    model = RefundOrder
    paginate_by = 20
    filterset_class = RefundFilter

# FUNCTION TO CREATE THE PICKLIST PDF FROM PICKLIST HTML FILE
def picklist_create(request, id):
    try: 
        shipment = OrderShipment.objects.filter(order_id=id).latest('pk')
    except ObjectDoesNotExist: 
        shipment = 'null'

    context = { 
            'order': Order.objects.get(order_id=id),
            'order_items': OrderItem.objects.filter(order_id=id).order_by('-send_qty', 'product_id__location'),
            'shipment': shipment,
        }
    return render(request, 'app_orders/order_detail/pdfs/picklist-create.html', context )

# FUNCTION TO CREATE THE INVOICE PDF FROM INVOICE HTML FILE
def invoice_create(request, id):

    context = { 
            'order': Order.objects.get(order_id=id),
        }
    return render(request, 'app_orders/order_detail/pdfs/invoice-create.html', context )

# FUNCTION TO CREATE THE INVOICE PDF FROM INVOICE HTML FILE
def credit_note_create(request, id):

    refundorder_id = RefundOrder.objects.filter(order_id=id)[0]
    items_total = RefundOrderItem.objects.filter(refundorder_id=refundorder_id).aggregate(Sum('total_price'))['total_price__sum'] or 0.00
    vat = float(items_total) * 0.2

    context = { 
            'refundorder': RefundOrder.objects.filter(order_id=id)[0],
            'items_total': items_total,
            'vat' : vat,
        }
    return render(request, 'app_orders/order_detail/pdfs/credit-note-create.html', context )


