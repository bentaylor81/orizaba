import django_filters
from .models import *

class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = {
            'order_no' : ['contains'],
            'delivery_name' : ['icontains'],
            'delivery_email' : ['icontains'],
            'status_current': ['exact'],
        }