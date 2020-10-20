from django.conf import settings
from app_products.models import *
from app_orders.models import *
from django.db.models import Subquery, OuterRef, DecimalField, IntegerField, Sum, Count

# STOCK MOVEMENT ORDER - CREATE A ROW IN THE StockMovement TABLE WHEN AN ITEM IS ADDED TO THE ORDERITEM TABLE 
def stock_movement_order(request):
    orderitems = OrderItem.objects.filter(stock_movement_added=False)

    for orderitem in orderitems:
        # Get currenct stock qty from product table - orizaba_stock_qty
        p_id = orderitem.product_id.product_id
        product = Product.objects.get(pk=p_id)       
        # Add current stock qty to orderitem qty
        current_stock_qty = int(product.orizaba_stock_qty) - int(orderitem.item_qty) 
        # Set the stock qty in Product table (orizaba_stock_qty) to the new rolling stock qty in stock movement table
        Product.objects.filter(pk=p_id).update(orizaba_stock_qty=current_stock_qty)
        # Add a row in Stock Movement table, which calculates a rolling stock figure
        StockMovement.objects.create(
            product_id=orderitem.product_id, 
            adjustment_qty=-orderitem.item_qty, 
            movement_type="Online Sale",
            order_id=orderitem.order_id,
            current_stock_qty=current_stock_qty
            # Add in date function here
            )  
        # date_added=orderitem.order_id.date - add this above if you want to update date 
        # Set the sotck movement_added field to true, so that this doesn't get added more than once
        orderitem.stock_movement_added = True
        orderitem.save()
    return ()

# RESET FUNCTIONS #
# SET All ORDERITEMS STOCK_MOVEMENT_ADDED TO FALSE 
def stock_movement_added_false(request):
    orderitem = OrderItem.objects.all()
    for item in orderitem:
        item.stock_movement_added = False
        item.save()
    return ()