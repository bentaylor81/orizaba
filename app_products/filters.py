import django_filters
from .models import *

class ProductFilter(django_filters.FilterSet):

    Product = django_filters.CharFilter(field_name='product_name', label='Product', lookup_expr='icontains')
    Sku = django_filters.CharFilter(field_name='sku', label='SKU', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['Product', 'Sku', 'brand', 'supplier']
        

class SupplierProductFilter(django_filters.FilterSet):
    
    class Meta:
        model = Product
        fields = {
            'product_name' : ['icontains'], 
            'sku' : ['icontains'],
            'brand': ['exact'],
        }
