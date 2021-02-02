from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from app_products.models import *
from app_orders.models import *
from app_utils.models import *
from django.utils import timezone
import datetime
import requests
import json
import pdfkit
import wkhtmltopdf
import time

# PRINT PRODUCT LABEL - USED IN PRODUCT LIST AND PURCHASE ORDER DETAIL
def printProductLabel(request):
    # FILTER PRODUCTS TO PRINT
    products = ProductLabel.objects.filter(is_printed=False)
    now = datetime.datetime.now(tz=timezone.utc)
    # GET PRINT PROCESS
    process = PrintProcess.objects.get(process_id=3)
    # LOOP TO PRINT LABELS
    for product in products: 
        # GET VARS
        product_id = product.product.product_id
        sku = product.product.sku
        qty = product.qty
        printer_id = process.process_printer.printnode_id   
        # GENERATE A PDF FILE IN STATIC 
        wkhtmltopdf_config = settings.WKHTMLTOPDF_CMD
        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_config)
        options = {'copies' : '1', 'page-width' : '51mm', 'page-height' : '102mm', 'orientation' : 'Landscape', 'margin-top': '0', 'margin-right': '0', 'margin-bottom': '0', 'margin-left': '0', } 
        projectUrl = 'http://' + request.get_host() + '/product/label/%s' % product_id
        pdf = pdfkit.from_url(projectUrl, "static/pdf/product-label.pdf", configuration=config, options=options)   
        # SEND TO PRINTNODE
        payload = '{"printerId": '+str(printer_id)+', "title": "Label for: ' +str(sku)+ ' ", "contentType": "pdf_uri", "content":"https://orizaba.herokuapp.com/static/pdf/product-label.pdf", "source": "GTS Product Label", "options": {"copies": ' +str(qty)+ '}}'
        response = requests.request("POST", "https://api.printnode.com/printjobs", headers=settings.PRINTNODE_HEADERS, data=payload)
        print(response.text.encode('utf8'))
        # SET IS_PRINTED TO TRUE
        product.is_printed = True
        product.date_printed = now
        product.save()
    return()