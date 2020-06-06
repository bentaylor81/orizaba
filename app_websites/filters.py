import django_filters
from .models import *

class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = {
            'order_no' : ['contains'],
            'delivery_name' : ['contains'],
            'delivery_email' : ['contains'],
        }

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'product_name' : ['contains'], 
            'sku' : ['contains'],
            'brand': ['exact'],
            'supplier': ['exact'],
        }

class SupplierProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'product_name' : ['contains'], 
            'sku' : ['contains'],
            'brand': ['exact'],
        }

