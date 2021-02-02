from django_filters import rest_framework as filters
from django import forms
from app_orders.models import *
from app_products.models import *
from app_utils.models import *

class StockMovementFilter(filters.FilterSet):
    class Meta:
        model = StockMovement
        fields = ['product_id__sku', 'movement_type']

class ApiLogFilter(filters.FilterSet):

    SERVICE_CHOICES = [
        ('Magento', 'Magento'),
        ('Mailgun', 'Mailgun'),
        ('Sagepay', 'Sagepay'),  
        ('Ship Theory', 'Ship Theory'),
        ('Xero', 'Xero'),
    ]

    api_service = filters.ChoiceFilter(field_name='api_service', label='Service Name', choices=SERVICE_CHOICES)     
    date = filters.DateFilter(field_name='date', lookup_expr='lte', label='Date To', widget=forms.DateInput(attrs={'type': 'date', 'class': 'date-input', 'id':'dateFromInput'}))
    response_code = filters.CharFilter(field_name='response_code', label='Response', lookup_expr='icontains')

    class Meta:
        model = ApiLog
        fields = ['process', 'api_service', 'response_code', 'date']