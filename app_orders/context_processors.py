from django.conf import settings
from app_products.models import *
from app_orders.models import *
from django.db.models import Subquery, OuterRef, DecimalField, IntegerField, Sum, Count
import pdfkit
import wkhtmltopdf

# CREATE INITIAL STATUS IN ORDERSTATUS HISTORY TABLE WHEN ORDER IS CREATED
# SET STATUS_UPDATED FIELD IN ORDER TABLE TO TRUE
def initial_status(request):
    orders = Order.objects.filter(initial_status_added=False, date__gt="2021-01-01")
    type_inst = OrderStatusType.objects.get(pk=10)

    for order in orders:
        OrderStatusHistory.objects.create(order_id=order, status_type=type_inst, date=order.date) 
        order.initial_status_added = True
        order.save()
    return()



