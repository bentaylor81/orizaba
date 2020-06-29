from app_websites.models import *
from app_orders.models import *
from django.db.models import Subquery, OuterRef, DecimalField, IntegerField, Sum, Count

def initial_status(request):

    orders = Order.objects.all().filter(status_updated=False)

    for i in orders:
        OrderStatusHistory.objects.create(order_id=i.order_id, status_type=10) 
        i.status_updated = True
        i.save()

    return ()