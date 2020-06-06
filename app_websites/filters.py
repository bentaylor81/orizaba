import django_filters
from .models import *

class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = {
            'order_no' : ['contains'],
            'delivery_name' : ['icontains'],
            'delivery_email' : ['icontains'],
        }

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'product_name' : ['icontains'], 
            'sku' : ['icontains'],
            'brand': ['exact'],
            'supplier': ['exact'],
        }

class SupplierProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'product_name' : ['icontains'], 
            'sku' : ['icontains'],
            'brand': ['exact'],
        }

