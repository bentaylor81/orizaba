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
