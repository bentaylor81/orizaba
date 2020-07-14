import django_filters
from .models import *

class OrderFilter(django_filters.FilterSet):

    Order = django_filters.CharFilter(field_name='order_no', label='Order Number', lookup_expr='icontains')
    BillingName = django_filters.CharFilter(field_name='billing_name', label='Billing Name', lookup_expr='icontains')

    class Meta:
        model = Order
        fields = ['Order', 'BillingName']