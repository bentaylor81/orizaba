from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Subquery, OuterRef, DecimalField, IntegerField, Sum, Count
from app_products.models import *
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
import requests
import json
import pdfkit
import wkhtmltopdf
from django_q.tasks import async_task

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
        # REFRESHES THE SHIPTHEORY TOKEN ASYNCRONOUSLY
        async_task("app_utils.services.shiptheory_token_task", 5, hook="app_utils.services.hook_after_sleeping")
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
            if shipment_no != 0:
                reference = str(order_no) + '/' + str(shipment_no)
            else: 
                reference = str(order_no)
            # SUBMIT THE FORM
            if form.is_valid():
                form.instance.order_id = form_order_id
                form.instance.shipping_ref = reference
                firstname = form['delivery_firstname'].value()
                lastname = form['delivery_lastname'].value()
                address_1 = form['delivery_address_1'].value()
                address_2 = form['delivery_address_2'].value()
                city = form['delivery_city'].value()
                postcode = form['delivery_postcode'].value()
                phone = form['delivery_phone'].value()
                email = form['delivery_email'].value()
                total_price = form['total_price_ex_vat'].value()  
                weight = form['weight'].value()  
                service_id = form['service_id'].value() 
                form.save()
                # ADD THE SHIPMENT CREATED AND PICKLIST PRINTED STATUS TO ORDER STATUS HISTORY TABLE
                order_inst = Order.objects.get(order_id=order_id)
                type_inst = OrderStatusType.objects.get(pk=20)
                OrderStatusHistory.objects.create(order_id=order_inst, status_type=type_inst) # SHIPMENT STATUS
                # SET THE STATUS IN THE ORDER TABLE TO SHIPMENT CREATED
                order_inst.status_current = type_inst
                order_inst.save()
                # CREATE SHIPTHEORY SHIPMENT
                payload = '{"reference":"'+str(reference)+'","reference2":"GTS","delivery_service":"'+service_id+'","increment":"1","shipment_detail":{"weight":"'+weight+'","parcels":1,"value":'+str(total_price)+'},"recipient":{"firstname":"'+firstname+'","lastname":"'+lastname+'","address_line_1":"'+address_1+'","address_line_2":"'+address_2+'","city":"'+city+'","postcode":"'+postcode+'","country":"GB","telephone":"'+phone+'","email":"'+email+'"}}'
                response = requests.request("POST", settings.ST_URL, headers=settings.ST_HEADERS, data=payload)
                print(payload)
                print(response.text)  
                # PRINT THE PICKLIST IF PICKLIST CHECKBOX IS TRUE
                picklist = form['picklist'].value()
                if picklist == True:
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
            # SEND TO PRINTNODE
            payload = '{"printerId": ' +str(settings.PRINTNODE_DESKTOP_PRINTER_OFFICE)+ ', "title": "Invoice for: ' +str(order_no)+ ' ", "contentType": "pdf_uri", "content":"https://orizaba.herokuapp.com/static/pdf/invoice.pdf", "source": "GTS Order Invoice"}'
            response = requests.request("POST", settings.PRINTNODE_URL, headers=settings.PRINTNODE_HEADERS, data=payload)
            print(response.text.encode('utf8'))
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
                messages.success(self.request, 'Invoice has been emailed to ' + to_email)
            else: 
                print(form.errors)
                messages.error(self.request, 'Invoice not sent as the form has errors')

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('order-detail', kwargs={'pk': self.object.pk})

    def print_picklist(self, request):
        # GENERATE THE PDF PICKLIST
        order_id = self.object.order_id
        order_no = self.object.order_no
        projectUrl = 'http://' + request.get_host() + '/orders/%s/picklist' % order_id
        pdf = pdfkit.from_url(projectUrl, "static/pdf/picklist.pdf", configuration=settings.WKHTMLTOPDF_CONFIG)
        # SEND TO PRINTNODE
        payload = '{"printerId": ' +str(settings.PRINTNODE_PRINT_TO_PDF)+ ', "title": "Picking List for: ' +str(order_no)+ '", "color": "true", "contentType": "pdf_uri", "content":"https://orizaba.herokuapp.com/static/pdf/picklist.pdf"}'
        response = requests.request("POST", settings.PRINTNODE_URL, headers=settings.PRINTNODE_HEADERS, data=payload)
        print(response.text.encode('utf8'))
        return 

    def shiptheory_token(self, request):
        # Generate the Auth Token
        url = settings.ST_URL_TOKEN
        payload='{"email": "'+settings.ST_USERNAME+'", "password": "'+settings.ST_PASSWORD+'"}'
        response = requests.request("POST", url, headers=settings.ST_HEADERS, data=payload)
        token = json.loads(response.text)['data']['token']
        heroku_token = 'Bearer ' + token
        # Update Heroku with Config Vars
        url = settings.HEROKU_URL_CONFIG_VARS
        auth = settings.HEROKU_BEARER_TOKEN
        payload='{"ST_AUTH":"'+heroku_token+'"}'
        headers = {'Content-Type': 'application/json', 'Accept': 'application/vnd.heroku+json; version=3', 'Authorization': auth, }
        response = requests.request("PATCH", url, headers=headers, data=payload)
        return

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
    
