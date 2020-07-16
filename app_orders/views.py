from django_tables2 import SingleTableView
from django.shortcuts import render, redirect
from django.db.models import Subquery, OuterRef, DecimalField, IntegerField, Sum, Count
from app_websites.models import *
from app_stats.models import *
from .filters import *
from django.contrib.auth.decorators import login_required
from app_users.decorators import unauthenticated_user, allowed_users
from django.core.paginator import Paginator
from .forms import OrderNoteForm
from django.contrib import messages
from django.views.generic import ListView
from django_filters.views import FilterView
from .tables import OrderTable

class OrderListView(FilterView):
    template_name = 'orders.html'
    model = Order
    paginate_by = 1
    filterset_class = OrderFilter
    strict = False
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tabs'] = OrderNavTab.objects.all()
        context['current_path'] = self.request.get_full_path()
        return context

# For Django Tables 2 - Currently not in use
class Order2ListView(SingleTableView):
    model = Order
    table_class = OrderTable
    template_name = 'orders2.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tabs'] = OrderNavTab.objects.all()
        context['current_path'] = self.request.get_full_path()
        return context



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def order_view(request, id):

    context = {
        'order' : Order.objects.get(order_no=id),
        'order_items' : OrderItem.objects.filter(order_id__order_no=id).order_by('order_id', '-active'),
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def order_view_update(request):

    if request.method == 'POST':
        form = OrderItem(request.POST or None)
        form.save(request)
        return render(request, 'order-view.html', context)
    else:
        return render(request, 'order-view.html', context)
