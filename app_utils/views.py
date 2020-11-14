from django.conf import settings
from django.shortcuts import render
from app_products.models import *
from app_orders.models import *
from .filters import *
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
import requests
import json


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
    return HttpResponseRedirect('/utils/stock-sync')

# UPDATE THE DATE IN STOCK MOVEMENT WITH THE ORDER DATE
# Function won't be needed in future when the date_added will be the order date
# Times out so needs a filter on there before running again. 
def update_stock_movement_date(request):
    stock_movement = StockMovement.objects.filter(movement_type="Online Sale")
    for product in stock_movement:
        if product.order_id:
            product.date_added = product.order_id.date
            product.save()
    return render(request, 'app_utils/utils.html')

# SEPARATE NAME AND SPLIT TO FIRST NAME / LAST NAME
def set_firstname_lastname(request):
    orders = Order.objects.filter(billing_firstname='')

    for order in orders:
        billing_name_split = order.billing_name.split()
        order.billing_firstname = billing_name_split[0]
        if len(billing_name_split) > 1:  
            order.billing_lastname = billing_name_split[1]

        delivery_name_split = order.delivery_name.split()
        order.delivery_firstname = delivery_name_split[0]
        if len(delivery_name_split) > 1:      
            order.delivery_lastname = delivery_name_split[1]
            
        order.save()
    return render(request, 'app_utils/utils.html')

### SHIPTHEORY TOKEN ###
# REFRESH THE BEARER TOKEN AND ADD TO CONFIG VARS IN HEROKU
def shiptheory_token(request):
    # Generate the Auth Token
    url = settings.ST_URL_TOKEN
    payload='{"email": "'+settings.ST_USERNAME+'", "password": "'+settings.ST_PASSWORD+'"}'
    response = requests.request("POST", url, headers=settings.ST_HEADERS, data=payload)
    token = json.loads(response.text)['data']['token']
    heroku_token = 'Bearer ' + token
    # Update Heroku with Config Vars
    url = settings.HEROKU_URL_CONFIG_VARS
    auth = settings.HEROKU_BEARER_TOKEN
    payload='{"ST_AUTH":"'+heroku_token+'"}'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/vnd.heroku+json; version=3', 'Authorization': auth, }
    response = requests.request("PATCH", url, headers=headers, data=payload)
    return render(request, 'app_utils/utils.html')

### STOCK RECONCILE PAGE ###
# LIST ALL STOCK MOVEMENTS - ORDERS, POS AND MANUAL ADJUSTMENTS
class StockMovementList(LoginRequiredMixin, FilterView):
    login_url = '/login/'
    template_name = 'app_utils/stock-reconcile.html'
    queryset = StockMovement.objects.all()
    model = StockMovement
    paginate_by = 50
    ordering = ['unleashed_status', '-date_added']
    filterset_class = StockMovementFilter

### STOCK SYNC PAGE ###
# CHECK THE STOCK SYNCRONIZATION BETWEEN MAGENTO AND ORIZABA
class StockSync(LoginRequiredMixin, FilterView):
    login_url = '/login/'
    template_name = 'app_utils/stock-sync.html'
    queryset = Product.objects.filter(stock_balances=False)
    paginate_by = 50
    filterset_class = StockSyncFilter
    ordering = ['stock_balances', '-stock_discrepancy']



