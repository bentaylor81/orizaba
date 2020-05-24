from django.shortcuts import render
from django.db.models import Sum
from .models import *
from django.contrib.auth.decorators import login_required
from app_users.decorators import unauthenticated_user, allowed_users

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def orders(request):
        context = { 
                'orders' : Order.objects.all(),
                }
        return render(request, 'app_websites/orders.html', context )

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def order_view(request, id):
        
        items_total = OrderItem.objects.aggregate(Sum('total_price'))['total_price__sum']
        order = Order.objects.get(order_id=id)
        postage = order.delivery_price
        total_ex_vat = items_total + postage
        vat = round(float(total_ex_vat) * 0.2, 2)
        total_inc_vat = round(float(total_ex_vat) + vat, 2)

        context = {
                'order' : Order.objects.get(order_id=id),
                'order_items' : OrderItem.objects.filter(order_id=id),
                'items_total' : items_total,
                'postage' : postage,
                'vat' : vat,
                'total_ex_vat' : total_ex_vat,
                'total_inc_vat' : total_inc_vat,
                }
        return render(request, 'app_websites/order-view.html', context )
