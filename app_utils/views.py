from django.shortcuts import render
from app_products.models import *
from app_orders.models import *
from django.http import HttpResponseRedirect


def utils(request): 
    return render(request, 'app_utils/utils.html')

# RESET FUNCTION - RUN THIS FUNCTION TO SET THE STOCK IN ORIZABA TO THE STOCK IN UNLEASHED
# ORIZABA_INITIAL_STOCK_QTY = STOCK_QTY - FUNCTION TO SET THIS, CAN BE TURNED OFF ONCE RAN INITIALLY
def orizaba_stock_reset(request):
    products = Product.objects.all()
    for product in products:
        product.orizaba_stock_qty = product.stock_qty
        product.save()
    return render(request, 'app_utils/utils.html')

# RESET FUNCTION - RUN THIS FUNCTION TO SET THE CURRENT STOCK QUANTITY IN THE STOCK MOVEMENT TABLE TO NULL
# Might need to filter rows already null if this function slows down.
def current_stock_qty_null(request):
    stock_movement = StockMovement.objects.all()
    for product in stock_movement:
        product.current_stock_qty = None
        product.save()
    return render(request, 'app_utils/utils.html')

# UPDATE STOCK DISCREPANCY STATS - USED IN THE STOCK LIST IN PRODUCTS
def update_stock_descrepancy_stats(request):
    # Check that Unleased stock and Orizaba calculated stock balances     
    products = Product.objects.all()
    for product in products:
        product.stock_discrepancy = (product.stock_qty - product.orizaba_stock_qty)  
        if product.stock_discrepancy != 0:
            product.stock_balances = False
        else:
            product.stock_balances = True
        product.save()
    return HttpResponseRedirect('/stock')

# UPDATE THE DATE IN STOCK MOVEMENT WITH THE ORDER DATE
# Function won't be needed in future when the date_added will be the order date
def update_stock_movement_date(request):
    stock_movement = StockMovement.objects.all()
    for product in stock_movement:
        if product.order_id:
            product.date_added = product.order_id.date
            product.save()
    return render(request, 'app_utils/utils.html')