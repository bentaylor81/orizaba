from django.conf import settings
from app_products.models import *
from app_orders.models import *
from django.db.models import Subquery, OuterRef, DecimalField, IntegerField, Sum, Count

# STOCK MOVEMENT ORDER - CREATE A ROW IN THE StockMovement TABLE WHEN AN ITEM IS ADDED TO THE ORDERITEM TABLE 
def stock_movement_order(request):
    orderitems = OrderItem.objects.filter(stock_movement_added=False, order_id__date__gt="2021-01-01")
    for item in orderitems:
        new_stock_qty = int(item.product_id.orizaba_stock_qty) - int(item.item_qty) 
        # STOCKMOVEMENT TABLE - CALCULATE THE ROLLING STOCK FIGURE
        StockMovement.objects.create(product_id=item.product_id, adjustment_qty=-item.item_qty, movement_type="Online Sale", order_id=item.order_id, current_stock_qty=new_stock_qty, date_added=item.order_id.date)   
        # PRODUCT TABLE - UPDATE ORIZABA_STOCK_QTY TO NEW STOCK QTY
        item.product_id.orizaba_stock_qty = new_stock_qty
        item.product_id.save()  
        # ORDERITEM TABLE - STOCK_MOVEMENT_ADDED FIELD TO TRUE
        item.stock_movement_added = True
        item.save()
    return()