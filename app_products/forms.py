from django import forms
from .models import *
import requests
import json
from django.forms import inlineformset_factory

### PRODUCT LIST PAGE ###
class ProductLabelForm(forms.Form):
    sku = forms.CharField(max_length=20)
    product_name = forms.CharField(max_length=20)
    location = forms.CharField(max_length=20)
    qty = forms.IntegerField()
    path = forms.CharField(max_length=50)

### PRODUCT DETAIL PAGE ###
class ProductDetailForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['status', 'product_name', 'sku', 'brand', 'supplier', 'sealed_item', 'weight', 'product_image', 'has_image']

class PurchaseOrderCreateForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['reference', 'supplier_reference', 'supplier', 'status', 'date_ordered']

class ManualStockAdjustForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['product', 'movement_type', 'adjustment_qty', 'current_stock_qty', 'comments']

### PURCHASE ORDER LIST PAGE ###
class PurchaseOrderCreateForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['reference', 'supplier_reference', 'supplier', 'status', 'date_ordered']
 
### PURCHASE ORDER DETAIL PAGE ###
class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['status', 'notes', 'reference', 'supplier', 'supplier_reference', 'date_ordered']