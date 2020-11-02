from django_filters import rest_framework as filters
from app_orders.models import *
from app_products.models import *

class StockMovementFilter(filters.FilterSet):
    class Meta:
        model = StockMovement
        fields = ['product_id__sku', 'movement_type']

class StockSyncFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'sku' : ['icontains'],
            'stock_discrepancy': ['exact'],
        }