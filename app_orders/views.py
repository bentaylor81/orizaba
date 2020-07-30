from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Subquery, OuterRef, DecimalField, IntegerField, Sum, Count
from app_websites.models import *
from app_stats.models import *
from .filters import *
from django.contrib.auth.decorators import login_required
from app_users.decorators import unauthenticated_user, allowed_users
from django.core.paginator import Paginator
from .forms import OrderDeliveryDetailsForm, OrderNoteForm, OrderForm, OrderItemFormset
from .utils import *
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.views.generic import ListView, DetailView, FormView, UpdateView
from django.views.generic.edit import FormMixin
from django_filters.views import FilterView
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.urls import reverse, reverse_lazy
import requests
import json
import pdfkit
import wkhtmltopdf

class OrderList(FilterView):
    template_name = 'app_orders/order-list.html'
    model = Order
    paginate_by = 20
    filterset_class = OrderFilter
    strict = False
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tabs'] = OrderNavTab.objects.all()
        context['current_path'] = self.request.get_full_path()
        return context

class OrderDetail(DetailView):
    template_name = 'app_orders/order-detail.html'
    queryset = Order.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Order, order_id=id_)

class OrderDeliveryEdit(SuccessMessageMixin, UpdateView):
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

class OrderPicklistEdit(SuccessMessageMixin, UpdateView):
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
        self.object = form.save()
        order_item_form.instance = self.object
        order_item_form.save()
        # Generate PDF Picklist
        self.generate_picklist(self.request)
        messages.success(self.request, 'Picking List Printed')
        return HttpResponseRedirect(self.get_success_url())

    def generate_picklist(self, request):
        # Generate the PDF
        wkhtmltopdf_config = settings.WKHTMLTOPDF_CMD
        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_config)
        order_no = self.object.order_id
        projectUrl = 'http://' + request.get_host() + '/orders/%s/picklist' % order_no # Need to un-hardcode
        pdf = pdfkit.from_url(projectUrl, "static/pdf/picklist.pdf", configuration=config)
        # Send to PrintNode
        url = settings.PRINTNODE_URL
        auth = settings.PRINTNODE_AUTH
        printer = settings.PRINTNODE_DESKTOP_PRINTER
        payload = '{"printerId": ' +str(printer)+ ', "title": "Picking List for: Ben", "contentType": "pdf_uri", "content":"https://orizaba.herokuapp.com/static/pdf/picklist.pdf"}'
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

