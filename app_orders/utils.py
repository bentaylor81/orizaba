from django.conf import settings
from app_products.models import *
from app_orders.models import *
from .views import *
import wkhtmltopdf
import pdfkit
import requests


def email_invoice():
    print('Hello Ben')
   
    url = ""

    payload = {}
    headers = {
            'xero-tenant-id': '',
            'Authorization': '',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Cookie': ''
    }

    response = requests.request("POST", url, headers=headers, data = payload)

    print(response.text.encode('utf8'))

def create_picklist(self, request):
    print('Hello Bennyt')
    order_id = generate_picklist()

    wkhtmltopdf_config = settings.WKHTMLTOPDF_CMD
    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_config)
    projectUrl = 'http://' + request.get_host() + '/orders/%s/picklist' % order_id
    pdf = pdfkit.from_url(projectUrl, "static/pdf/picklist.pdf", configuration=config)
    # Send to PrintNode
    url = settings.PRINTNODE_URL
    auth = settings.PRINTNODE_AUTH
    printer = settings.PRINTNODE_DESKTOP_PRINTER
    payload = '{"printerId": ' +str(printer)+ ', "title": "Picking List for: ' +str(order_no)+ '", "color": "true", "contentType": "pdf_uri", "content":"https://orizaba.herokuapp.com/static/pdf/picklist.pdf"}'
    
    #headers = {'Content-Type': 'application/json', 'Authorization': auth, }
    #response = requests.request("POST", url, headers=headers, data=payload)
    #print(response.text.encode('utf8'))