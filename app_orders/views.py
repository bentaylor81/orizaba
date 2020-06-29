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


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def orders(request):

    orders = Order.objects.all()
    # Order Filtering
    orderFilter = OrderFilter(request.GET, queryset=orders)
    orders = orderFilter.qs
    # Order Pagination
    paginator = Paginator(orders, 10)
    page = request.GET.get('page')
    items = paginator.get_page(page)

    context = { 
        'orders' : orders,
        'items' : items,
        'orderFilter' : OrderFilter()
        }
            
    return render(request, 'app_orders/orders.html', context )

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def order_view(request, id):

    context = {
        'order' : Order.objects.get(order_no=id),
        'order_items' : OrderItem.objects.filter(order_id__order_no=id),
        'status_history' : OrderStatusHistory.objects.filter(order_id__order_no=id),
        'notes' : OrderNote.objects.filter(order_id__order_no=id),
        'current_user' : request.user,
        }

    if request.method == 'POST':
        form = OrderNoteForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, ('Note has been added'))
            return render(request, 'app_orders/order-view.html', context)
        else: 
            messages.error(request, ('Note cannot be blank'))
            return render(request, 'app_orders/order-view.html', context)
    else:
        return render(request, 'app_orders/order-view.html', context)