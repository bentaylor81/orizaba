from django.conf import settings
from django.shortcuts import render
from app_orders.views import *
import rollbar
import requests
import json
import pdfkit
import wkhtmltopdf

### SHIPTHEORY TOKEN ###
# REFRESH THE BEARER TOKEN AND ADD TO CONFIG VARS IN HEROKU
def shiptheory_token_task(request):
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
    print('######')
    print("ShipTheory Bearer Token Task Complete")
    print('######')

def shiptheory_token_task_hook(task):
    print(task.result)

### XERO TOKEN ###
# REFRESH THE BEARER TOKEN AND ADD TO CONFIG VARS
def xero_token_task(request):
    # Refresh the Xero Access Token
    url = "https://identity.xero.com/connect/token?="
    payload = {'grant_type': 'refresh_token','refresh_token': settings.XERO_REFRESH_TOKEN,'client_id': settings.XERO_CLIENT_ID,'client_secret': settings.XERO_CLIENT_SECRET,}
    response = requests.request("POST", url, data=payload)
    token = json.loads(response.text)['id_token']
    xero_token = 'Bearer ' + token
    # Update Heroku with Config Vars
    url = settings.HEROKU_URL_CONFIG_VARS
    auth = settings.HEROKU_BEARER_TOKEN
    payload='{"XERO_AUTH":"'+xero_token+'"}'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/vnd.heroku+json; version=3', 'Authorization': auth, }
    response = requests.request("PATCH", url, headers=headers, data=payload)
    print('######')
    print("Xero Token Task Complete")
    print('######')




### CURRENTLY NOT ACTIVE ###
def print_picklist_task(order_id):
    order = Order.objects.get(order_id=order_id)
    order_no = order.order_no    
    # # GENERATE THE PDF PICKLIST
    # wkhtmltopdf_config = settings.WKHTMLTOPDF_CMD
    # config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_config)
    # projectUrl = settings.HOST_URL + '/orders/%s/picklist' % order_id
    # pdf = pdfkit.from_url(projectUrl, "static/pdf/picklist.pdf", configuration=config)
    # # SEND TO PRINTNODE
    # payload = '{"printerId": ' +str(settings.PRINTNODE_PRINT_TO_PDF)+ ', "title": "Picking List for: ' +str(order_no)+ '", "color": "true", "contentType": "pdf_uri", "content":"https://orizaba.herokuapp.com/static/pdf/picklist.pdf"}'
    # response = requests.request("POST", settings.PRINTNODE_URL, headers=settings.PRINTNODE_HEADERS, data=payload)
    # print(response.text.encode('utf8'))
    print(order_id)
    print(order.order_no)
    print('Print PDF Task Complete')
    print('######')
    print('Add Shipment Status')

def print_picklist_task_hook(task):
    print(task.result)

def create_shiptheory_shipment_task(shipping_ref):
    shipment = OrderShipment.objects.get(shipping_ref=shipping_ref)
    # EXTRACT THE SHIPMENT VARIABLES
    service_id = shipment.service_id.service_id 
    firstname = shipment.delivery_firstname
    lastname = shipment.delivery_lastname
    address_1 = shipment.delivery_address_1
    address_2 = shipment.delivery_address_2
    city = shipment.delivery_city
    postcode = shipment.delivery_postcode
    phone = shipment.delivery_phone
    email = shipment.delivery_email
    total_price = shipment.total_price_ex_vat
    weight = shipment.weight
    # CREATE SHIPTHEORY SHIPMENT
    payload = '{"reference":"'+str(shipping_ref)+'","reference2":"GTS","delivery_service":"'+str(service_id)+'","increment":"1","shipment_detail":{"weight":"'+weight+'","parcels":1,"value":'+str(total_price)+'},"recipient":{"firstname":"'+firstname+'","lastname":"'+lastname+'","address_line_1":"'+address_1+'","address_line_2":"'+address_2+'","city":"'+city+'","postcode":"'+postcode+'","country":"GB","telephone":"'+phone+'","email":"'+email+'"}}'
    response = requests.request("POST", settings.ST_URL, headers=settings.ST_HEADERS, data=payload)
    print('### CREATE SHIPTHEORY SHIPMENT TASK START ###')
    print(payload)
    print(response.text)  
    print('### CREATE SHIPTHEORY SHIPMENT TASK END ###') 

def create_shiptheory_shipment_hook(task):
    print(task.result)