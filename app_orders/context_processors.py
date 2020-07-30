from app_websites.models import *
from app_orders.models import *
from django.db.models import Subquery, OuterRef, DecimalField, IntegerField, Sum, Count

# Create the first status in OrderStatusHistory table when an order is created. 
def initial_status(request):

    orders = Order.objects.filter(status_updated=False)

    for order in orders:
        type_inst = OrderStatusType.objects.get(pk=10)
        OrderStatusHistory.objects.create(order_id=order, status_type=type_inst) 
        order.status_current = type_inst
        order.status_updated = True
        order.save()
    return ()

# When ran Sent Qty = Item Qty
# send_qty_init_updated field then set to true 
def initial_send_qty(request):

    orderitems = OrderItem.objects.filter(send_qty_init_updated=False) 

    for orderitem in orderitems:
        orderitem.send_qty = orderitem.item_qty
        orderitem.send_qty_init_updated = True
        orderitem.save()
    return ()