import django_filters
from .models import *

class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = ['order_no', 'delivery_name', 'delivery_email']

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['sku', 'product_name', 'brand', 'supplier']