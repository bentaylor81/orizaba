from django.shortcuts import render
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
        context = {
                'order' : Order.objects.get(pk=id),  
                }
        return render(request, 'app_websites/order-view.html', context )
