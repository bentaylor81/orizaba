from django import forms
from django_filters import rest_framework as filters
from .models import *

class ProductFilter(filters.FilterSet):

    STATUS_CHOICES = [
        ('Enabled', 'Enabled'),
        ('Disabled', 'Disabled'),
    ]

    Product = filters.CharFilter(field_name='product_name', label='Product', lookup_expr='icontains')
    Sku = filters.CharFilter(field_name='sku', label='SKU', lookup_expr='icontains')
    Stock_qty = filters.CharFilter(field_name='stock_qty', label='Stock Qty', widget=forms.NumberInput(attrs={'type': 'number', 'class': 'stock_qty_input'}))
    Status = filters.ChoiceFilter(field_name='status', label='Status', choices=STATUS_CHOICES)
    # stock_qty = filters.ChoiceFilter(choices=STOCK_CHOICES, label='Out of Stock')
    o = filters.OrderingFilter(
        choices=(
            ('brand', 'Brand'),
            ('-brand', 'Brand (desc)'),
            ('location', 'Location'),
            ('-location', 'Location (desc)'),
            ('product_name', 'Product Name'),
            ('-product_name', 'Product Name (desc)'),
            ('sell_price', 'Sell Price'),
            ('-sell_price', 'Sell Price (desc)'),
            ('sku', 'SKU'),
            ('-sku', 'SKU (desc)'),
            ('orizaba_stock_qty', 'Stock Qty'),
            ('-orizaba_stock_qty', 'Stock Qty (desc)'),
            ('supplier', 'Supplier'),
            ('-supplier', 'Supplier (desc)'),
            ('weight', 'Weight'),
            ('-weight', 'Weight (desc)'),
            ('last_stock_check', 'Last Stock Check'),
            ('-last_stock_check', 'Last Stock Check (desc)'),
        ),
        label='',
    )
    class Meta:
        model = Product
        fields = ['Product', 'Sku', 'brand', 'supplier', 'Stock_qty', 'has_image']
        
class PurchaseOrderFilter(filters.FilterSet):
    class Meta:
        model = PurchaseOrder
        fields = ['reference', 'supplier', 'status']

class SupplierProductFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'product_name' : ['icontains'], 
            'sku' : ['icontains'],
            'brand': ['exact'],
        }