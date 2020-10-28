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
import requests
import json
import pdfkit
import wkhtmltopdf

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
        context = super().get_context_data(**kwargs)
        context['delivery_methods'] = OrderDeliveryMethod.objects.all()
        return context

    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Order, order_id=id_)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        order_id = self.object.order_id
        order_no = self.object.order_no
        form_order_id = Order.objects.get(pk=order_id)
        
        if 'add-shipment' in request.POST:
            form_class = self.get_form_class()
            form = self.get_form(form_class)
 
            if form.is_valid():
                form.instance.order_id = form_order_id
                form.save()
                url = settings.PH_URL
                headers = settings.PH_HEADERS
                version = str(settings.PH_VERSION)
                account = str(settings.PH_ACCOUNT)
                service_info = str('<ServiceInfo><ServiceId>'+str(self.object.delivery_method.service_id)+'</ServiceId><ServiceCustomerUID>'+str(self.object.delivery_method.service_provider_uid)+'</ServiceCustomerUID><ServiceProviderId>'+str(self.object.delivery_method.service_provider_id)+'</ServiceProviderId></ServiceInfo>')
                delivery_address = str('<DeliveryAddress><ContactName>'+self.object.delivery_name+'</ContactName><Email>'+self.object.delivery_email+'</Email><Phone>'+self.object.delivery_phone+'</Phone><Address1>'+self.object.delivery_address_1+'</Address1><Address2>'+self.object.delivery_address_2+'</Address2><City>'+self.object.delivery_city+'</City><Postcode>'+self.object.delivery_postcode+'</Postcode><Country>GB</Country><AddressType>Business</AddressType></DeliveryAddress>')
                reference = '<Reference1>'+str(self.object.order_no)+'</Reference1><ContentsDescription>Machine Spare Parts</ContentsDescription><Packages><Package><PackageType>Parcel</PackageType><Value Currency=\"GBP\">'+str(self.object.total_price_inc_vat)+'</Value><Contents>Machine Spare Parts</Contents><Dimensions><Length>20</Length><Width>20</Width><Height>20</Height></Dimensions><Weight>2</Weight></Package></Packages>'
                payload = version + account + service_info + delivery_address + reference + '</Shipment>'
                response = requests.request("POST", url, headers=headers, data = payload)
                print(response.text.encode('utf8'))
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
                data = {'from': settings.MAILGUN_FROM, 'to': to_email, 'cc': settings.MAILGUN_CC, 'subject': form.data['subject'], 'html': form.data['message']}
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

class OrderPicklistEdit(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = '/login/'
    template_name = 'app_orders/order_detail/order-detail.html'
    model = Order
    form_class = OrderForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        order_item_form = OrderItemFormset(instance=self.object)
        return self.render_to_response(self.get_context_data(form=form, order_item_form=order_item_form))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        order_item_form = OrderItemFormset(self.request.POST, instance=self.object)
        if (order_item_form.is_valid() and form.is_valid()):
            return self.form_valid(form, order_item_form)
        else:
            return HttpResponse('Form Invalid')

    def form_valid(self, form, order_item_form):
        order_item_form.save()
        self.print_picklist(self.request)
        messages.success(self.request, 'Picking List Printed')
        return HttpResponseRedirect(self.get_success_url())

    def print_picklist(self, request):
        # GENERATE THE PDF PICKLIST
        wkhtmltopdf_config = settings.WKHTMLTOPDF_CMD
        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_config)
        order_id = self.object.order_id
        order_no = self.object.order_no
        projectUrl = 'http://' + request.get_host() + '/orders/%s/picklist' % order_id
        pdf = pdfkit.from_url(projectUrl, "static/pdf/picklist.pdf", configuration=config)
        # SEND TO PRINTNODE
        url = settings.PRINTNODE_URL
        auth = settings.PRINTNODE_AUTH
        printer = settings.PRINTNODE_DESKTOP_PRINTER
        payload = '{"printerId": ' +str(printer)+ ', "title": "Picking List for: ' +str(order_no)+ '", "color": "true", "contentType": "pdf_uri", "content":"https://orizaba.herokuapp.com/static/pdf/picklist.pdf"}'
        headers = {'Content-Type': 'application/json', 'Authorization': auth, }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text.encode('utf8'))
        return 

    def get_success_url(self):
        return reverse('order-detail', kwargs={'pk': self.object.pk})

# FUNCTION TO CREATE THE PICKLIST PDF FROM PICKLIST HTML FILE
def picklist_create(request, id):
    context = { 
            'order': Order.objects.get(order_id=id),
        }
    return render(request, 'app_orders/order_detail/pdfs/picklist-create.html', context )

# FUNCTION TO CREATE THE INVOICE PDF FROM INVOICE HTML FILE
def invoice_create(request, id):
    context = { 
            'order': Order.objects.get(order_id=id),
        }
    return render(request, 'app_orders/order_detail/pdfs/invoice-create.html', context )
    
