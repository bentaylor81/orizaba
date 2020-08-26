from django import forms
from django_filters import rest_framework as filters
from .models import *

class OrderFilter(filters.FilterSet):

    Order = filters.CharFilter(field_name='order_no', label='Order Number', lookup_expr='icontains')
    BillingName = filters.CharFilter(field_name='billing_name', label='Billing Name', lookup_expr='icontains')       
#    Date = filters.DateFromToRangeFilter(field_name='date', label=['Date From', 'to'])
    start_date = filters.DateFilter(field_name='date', lookup_expr=('gt'), label='Date From', widget=forms.DateInput(attrs={'type': 'date', 'class': 'date-input'}))
    end_date = filters.DateFilter(field_name='date', lookup_expr=('lt'), label='to', widget=forms.DateInput(attrs={'type': 'date', 'class': 'date-input'}))

    class Meta:
        model = Order
        fields = ['Order', 'BillingName', 'status_current', 'start_date', 'end_date']