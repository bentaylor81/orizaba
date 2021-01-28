from django.conf import settings
from django.shortcuts import render
from app_products.models import *
from app_orders.models import *
from app_utils.models import *
from .filters import *
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
import requests
import json
import os
import redis
from django_q.tasks import async_task

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

# GET THE TRACKING CODE FROM SHIPTHEORY
def shiptheory_tracking_code(request):
    url = "https://api.shiptheory.com/v1/shipments/search?created_from=2020-11-25&created_to=2020-11-26"
    payload={}
    response = requests.request("GET", url, headers=settings.ST_HEADERS, data=payload)
    #print(response.text)
    shipment_list = json.loads(response.text)
    # i = 0
    # while (i < len(shipment_list['shipments'])):
    #     print(shipment_list['shipments'][i]['delivery_address']['firstname'])
    #     print(shipment_list['shipments'][i]['delivery_address']['lastname'])
    #     print(shipment_list['shipments'][i]['courier']['couriername'])
    #     print(shipment_list['shipments'][i]['shipment_detail']['tracking_number'])
    #     print('################')
    #     i+=1
    order_shipment = OrderShipment.objects.filter(tracking_code='')
    print(order_shipment)

    for shipment in shipment_list['shipments']:
        if shipment['channel_reference_id'] == '308816':
            delivery_name = shipment['delivery_address']['firstname'] + ' ' + shipment['delivery_address']['lastname']
            tracking_no = shipment['shipment_detail']['tracking_number']
            print(delivery_name + ' ' + tracking_no)

    return HttpResponse(response.text)

### SHIPTHEORY TOKEN ###
# REFRESH THE BEARER TOKEN AND ADD TO CONFIG VARS IN HEROKU
def shiptheory_token(request):
    # Generate the Auth Token
    payload='{"email": "'+settings.ST_USERNAME+'", "password": "'+settings.ST_PASSWORD+'"}'
    response = requests.request("POST", "https://api.shiptheory.com/v1/token", headers=settings.ST_HEADERS, data=payload)
    token = json.loads(response.text)['data']['token']
    heroku_token = 'Bearer ' + token
    # Update Heroku with Config Vars
    url = settings.HEROKU_URL_CONFIG_VARS
    auth = settings.HEROKU_BEARER_TOKEN
    payload='{"ST_AUTH":"'+heroku_token+'"}'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/vnd.heroku+json; version=3', 'Authorization': auth, }
    response = requests.request("PATCH", url, headers=headers, data=payload)
    return render(request, 'app_utils/utils.html')

### XERO TOKEN ###
# REFRESH THE BEARER TOKEN AND ADD TO CONFIG VARS
def xero_token(request):
    # Refresh the Xero Access Token
    url = "https://identity.xero.com/connect/token?="
    payload = {'grant_type': 'refresh_token','refresh_token': settings.XERO_REFRESH_TOKEN,'client_id': settings.XERO_CLIENT_ID,'client_secret': settings.XERO_CLIENT_SECRET,}
    
    response = requests.request("POST", url, data=payload)
    print(response.text)
    access_token = json.loads(response.text)['access_token']
    refresh_token = json.loads(response.text)['refresh_token']
    xero_token = 'Bearer ' + access_token
    # Update Heroku with Config Vars
    url = settings.HEROKU_URL_CONFIG_VARS
    auth = settings.HEROKU_BEARER_TOKEN
    payload='{"XERO_AUTH":"'+xero_token+'", "XERO_REFRESH_TOKEN":"'+refresh_token+'"}'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/vnd.heroku+json; version=3', 'Authorization': auth, }
    response = requests.request("PATCH", url, headers=headers, data=payload)
    return render(request, 'app_utils/utils.html')

### REDIS CREDENTIALS ###
def redis_creds(request):
    return render(request, 'app_utils/utils.html')

    
### STOCK RECONCILE PAGE ###
# LIST ALL STOCK MOVEMENTS - ORDERS, POS AND MANUAL ADJUSTMENTS
class StockMovementList(LoginRequiredMixin, FilterView):
    login_url = '/login/'
    template_name = 'app_utils/stock-reconcile.html'
    queryset = StockMovement.objects.all()
    model = StockMovement
    paginate_by = 50
    ordering = ['-date_added']
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

### API LOG ###
class ApiLogList(LoginRequiredMixin, FilterView):
    login_url = '/login/'
    template_name = 'app_utils/api-log-list.html'
    model = ApiLog
    paginate_by = 50

### MAGENTO STOCK SYNC ###
class MagentoProductSync(LoginRequiredMixin, FilterView):
    login_url = '/login/'
    template_name = 'app_utils/magento-product-sync.html'
    model = MagentoProductSync
    paginate_by = 50

### SCRIPTS ###
def scripts(request):
    return render(request, 'app_utils/utils.html')