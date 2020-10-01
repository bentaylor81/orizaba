from django import forms
from .models import *
import requests
import json
from django.forms import inlineformset_factory

class ProductLabelForm(forms.Form):
    sku = forms.CharField(max_length=20)
    product_name = forms.CharField(max_length=20)
    location = forms.CharField(max_length=20)
    qty = forms.IntegerField()
    path = forms.CharField(max_length=50)

class PurchaseOrderCreateForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['reference', 'supplier_reference', 'supplier', 'status', 'date_ordered']
 
class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['status', 'notes', 'reference', 'supplier', 'supplier_reference', 'date_ordered']

PoItemFormset = inlineformset_factory(
    PurchaseOrder, 
    PurchaseOrderItem, 
    extra=0, 
    can_delete=True,
    fields=('product', 'purchaseorder', 'order_qty', 'delivery_qty', 'comments', 'date_updated'),
    widgets={
        'delivery_qty' : forms.NumberInput(attrs={'min': '0' }), 
        'product' : forms.TextInput(attrs={'type': 'hidden' }), 
        }
    )
    