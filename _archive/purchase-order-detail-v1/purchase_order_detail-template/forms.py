from django import forms
from .models import *
import requests
import json
from django.forms import inlineformset_factory

### PURCHASE ORDER DETAIL PAGE ###
class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['status', 'notes', 'reference', 'supplier', 'supplier_reference', 'date_ordered']

PoItemFormset = inlineformset_factory(
    PurchaseOrder, 
    PurchaseOrderItem, 
    extra=0, 
    can_delete=True,
    fields=('product', 'product_sku','purchaseorder', 'order_qty', 'delivery_qty', 'comments', 'label', 'date_updated'),
    widgets={
        'delivery_qty' : forms.NumberInput(attrs={'min': '0' }), 
        'product' : forms.TextInput(attrs={'type': 'hidden' }), 
        'product_sku' : forms.TextInput(attrs={'type': 'hidden' }), 
        'label' : forms.CheckboxInput (attrs={'class': 'label-checkbox' }), 
        }
    )
