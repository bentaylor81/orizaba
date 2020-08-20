from django import forms
from .models import *
import requests
import json

class ProductLabelForm(forms.Form):
    sku = forms.CharField(max_length=20)
    product_name = forms.CharField(max_length=20)
    location = forms.CharField(max_length=20)
    qty = forms.IntegerField()
    path = forms.CharField(max_length=50)


    def print_label(self):
        url = "https://api.printnode.com/printjobs"
        auth = 'Basic RzV0TkdoNlItMDJuUzM2U1NYcXJVaTFPOXZBNWN2WE9CNV8xeWFYb1Vrbzo='
        content = "test-label.pdf"
        title = "Hello Ben"
        printer = "69572913"
        copies = "10"

        payload = '{"printerId": ' +str(printer)+ ', "title": " ' +str(title)+ ' ", "contentType": "pdf_uri", "content":"https://orizaba.herokuapp.com/static/pdf/' +str(content)+ '", "source": "GTS Test Page", "options": {"copies": ' +str(copies)+ '}}'
        
        headers = {
                'Content-Type': 'application/json',
                'Authorization': auth,
        }

        response = requests.request("POST", url, headers=headers, data = payload)

        print(response.text.encode('utf8'))

 

