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

class OrderList(LoginRequiredMixin, FilterView):
    login_url = '/login/'
    template_name = 'app_orders/order-list.html'
    model = Order
    paginate_by = 20
    filterset_class = OrderFilter
    strict = False
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.request.user()
        return context

class OrderDetail(LoginRequiredMixin, FormMixin, DetailView):
    login_url = '/login/'
    template_name = 'app_orders/order-detail.html'
    queryset = Order.objects.all()
    form_class = OrderShipmentForm
    model = Order

    def get_object(self):
        #self.xero_api(self.request) # XERO API
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Order, order_id=id_)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        order_id = self.object.order_id
        form_order_id = Order.objects.get(pk=order_id)

        if 'add-shipment' in request.POST:
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            if form.is_valid():
                form.instance.order_id = form_order_id
                form.save()
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
        
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('order-detail', kwargs={'pk': self.object.pk})

    # def xero_api(self, request): # XERO API
    #     email_invoice() # XERO API


class OrderDeliveryEdit(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = '/login/'
    template_name = 'app_orders/order-detail.html'
    form_class = OrderDeliveryDetailsForm
    model = OrderItem
    queryset = Order.objects.all()
    success_message = 'Delivery Details Updated'

    def get_success_url(self):
        return reverse('order-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delivery_methods'] = OrderDeliveryMethod.objects.all()
        return context

class OrderPicklistEdit(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = '/login/'
    model = Order
    form_class = OrderForm
    template_name = 'app_orders/order-detail.html'

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
        #self.object = form.save() # Not sure why I need these 2 lines
        #order_item_form.instance = self.object
        order_item_form.save()
        # Generate PDF Picklist
        self.generate_picklist(self.request)
        messages.success(self.request, 'Picking List Printed')
        return HttpResponseRedirect(self.get_success_url())

    def generate_picklist(self, request):
        # Generate the PDF
        wkhtmltopdf_config = settings.WKHTMLTOPDF_CMD
        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_config)
        order_id = self.object.order_id
        order_no = self.object.order_no
        projectUrl = 'http://' + request.get_host() + '/orders/%s/picklist' % order_id
        pdf = pdfkit.from_url(projectUrl, "static/pdf/picklist.pdf", configuration=config)
        # Send to PrintNode
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









# Below is to be deleted
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def order_view(request, id):

    context = {
        'order' : Order.objects.get(order_no=id),
        'order_items' : OrderItem.objects.filter(order_id__order_no=id).order_by('order_id'),
        'status_history' : OrderStatusHistory.objects.filter(order_id__order_no=id),
        'notes' : OrderNote.objects.filter(order_id__order_no=id),
        'current_user' : request.user,
        }

    if request.method == 'POST':
        form = OrderNoteForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, ('Note has been added'))
            return render(request, 'order-view.html', context)
        else: 
            messages.error(request, ('Note cannot be blank'))
            return render(request, 'order-view.html', context)
    else:
        return render(request, 'order-view.html', context)

