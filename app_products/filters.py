from django_filters import rest_framework as filters
from .models import *

class ProductFilter(filters.FilterSet):

    Product = filters.CharFilter(field_name='product_name', label='Product', lookup_expr='icontains')
    Sku = filters.CharFilter(field_name='sku', label='SKU', lookup_expr='icontains')

    o = filters.OrderingFilter(

        choices=(
            ('location', 'Location'),
            ('-location', 'Location (desc)'),
            ('sell_price', 'Sell Price'),
            ('-sell_price', 'Sell Price (desc)'),
            ('sku', 'SKU'),
            ('-sku', 'SKU (desc)'),
            ('stock_qty', 'Stock Qty'),
            ('-stock_qty', 'Stock Qty (desc)'),
            ('weight', 'Weight'),
            ('-weight', 'Weight (desc)'),
        ),
    )

    class Meta:
        model = Product
        fields = ['Product', 'Sku', 'brand', 'supplier']
        

class SupplierProductFilter(filters.FilterSet):
    
    class Meta:
        model = Product
        fields = {
            'product_name' : ['icontains'], 
            'sku' : ['icontains'],
            'brand': ['exact'],
        }
