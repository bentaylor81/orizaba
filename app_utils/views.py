from django.shortcuts import render
from app_products.models import *
from app_orders.models import *


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
def current_stock_qty_null(request):
    stock_movement = StockMovement.objects.all()
    for product in stock_movement:
        product.current_stock_qty = None
        product.save()
    return render(request, 'app_utils/utils.html')