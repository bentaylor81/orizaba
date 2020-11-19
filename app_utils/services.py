from django.conf import settings
from django.shortcuts import render
from app_orders.views import *
import requests
import json
import pdfkit
import wkhtmltopdf

### SHIPTHEORY TOKEN ###
# REFRESH THE BEARER TOKEN AND ADD TO CONFIG VARS IN HEROKU
def shiptheory_token_task(request):
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
    print("ShipTheory Bearer Token Task Complete")

def hook_after_sleeping(task):
    print(task.result)

### CURRENTLY NOT ACTIVE ###
def print_picklist_task(order_id):
    order = Order.objects.get(order_id=order_id)
    order_no = order.order_no
    print('######')
    print(order_id)
    print(order_no)
    # # GENERATE THE PDF PICKLIST
    # wkhtmltopdf_config = settings.WKHTMLTOPDF_CMD
    # config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_config)
    # projectUrl = settings.HOST_URL + '/orders/%s/picklist' % order_id
    # pdf = pdfkit.from_url(projectUrl, "static/pdf/picklist.pdf", configuration=config)
    # # SEND TO PRINTNODE
    # payload = '{"printerId": ' +str(settings.PRINTNODE_PRINT_TO_PDF)+ ', "title": "Picking List for: ' +str(order_no)+ '", "color": "true", "contentType": "pdf_uri", "content":"https://orizaba.herokuapp.com/static/pdf/picklist.pdf"}'
    # response = requests.request("POST", settings.PRINTNODE_URL, headers=settings.PRINTNODE_HEADERS, data=payload)
    # print(response.text.encode('utf8'))
    print('Print PDF Task Complete')
    print('######')