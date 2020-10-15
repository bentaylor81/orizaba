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
            )   
        # Set the sotck movement_added field to true, so that this doesn't get added more than once
        orderitem.stock_movement_added = True
        orderitem.save()
    return ()

# ORIZABA_INITIAL_STOCK_QTY = STOCK_QTY - FUNCTION TO SET THIS, CAN BE TURNED OFF ONCE RAN INITIALLY
# RESET FUNCTION - RUN THIS FUNCTION TO SET THE STOCK IN ORIZABA TO THE STOCK IN UNLEASHED
def orizaba_stock_qty(request):
    products = Product.objects.all()
    for product in products:
        product.orizaba_stock_qty = product.stock_qty
        product.save()
    return ()

# RESET FUNCTION - RUN THIS FUNCTION TO SET THE CURRENT STOCK QUANTITY IN THE STOCK MOVEMENT TABLE TO NULL
def current_stock_qty_null(request):
    stock_movement = StockMovement.objects.all()
    for product in stock_movement:
        product.current_stock_qty = None
        product.save()
    return ()