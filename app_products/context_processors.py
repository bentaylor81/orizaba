from django.conf import settings
from app_products.models import *
from app_orders.models import *
from django.db.models import Subquery, OuterRef, DecimalField, IntegerField, Sum, Count

# STOCK MOVEMENT ORDER - CREATE A ROW IN THE StockMovement TABLE WHEN AN ITEM IS ADDED TO THE ORDERITEM TABLE 
def stock_movement_order(request):
    orderitems = OrderItem.objects.filter(stock_movement_added=False, order_id__date__gt="2021-01-01")
    for orderitem in orderitems:
        # GET CURRENT STOCK QTY FROM PRODUCT TABLE (ORIZABA_STOCK_QTY)
        p_id = orderitem.product_id.product_id
        product = Product.objects.get(pk=p_id)       
        # ADD CURRENT STOCK QTY TO ORDERITME QTY
        current_stock_qty = int(product.orizaba_stock_qty) - int(orderitem.item_qty) 
        # SET ORIZABA_STOCK_QTY IN PRODUCT TABLE TO NEW ROLLING STOCK QTY IN SOTCK MOVEMENT TABLE
        Product.objects.filter(pk=p_id).update(orizaba_stock_qty=current_stock_qty)
        # ADD ROW TO STOCK MOVEMENT TABLE TO CALCULATE THE ROLLING STOCK FIGURE
        StockMovement.objects.create(product_id=orderitem.product_id, adjustment_qty=-orderitem.item_qty, movement_type="Online Sale", order_id=orderitem.order_id, current_stock_qty=current_stock_qty, date_added=orderitem.order_id.date)   
        # SET THE STOCK MOVEMENT_ADDED FIELD TO TRUE
        orderitem.stock_movement_added = True
        orderitem.save()
    return ()