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
        fields = ['product_image']

class PurchaseOrderCreateForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['reference', 'supplier_reference', 'supplier', 'status', 'date_ordered']

class ManualStockAdjustForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['product_id', 'date_added', 'movement_type', 'adjustment_qty', 'current_stock_qty', 'comments']

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

### UNLEASHED PAGE ###
class UnleashedForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['id', 'unleashed_status']