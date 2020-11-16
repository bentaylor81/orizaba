from django import forms
from django_filters import rest_framework as filters
from .models import *

class OrderFilter(filters.FilterSet):

    order = filters.CharFilter(field_name='order_no', label='Order Number', lookup_expr='icontains')
    billing_last_name = filters.CharFilter(field_name='billing_lastname', label='Billing Surname', lookup_expr='icontains')       
#    Date = filters.DateFromToRangeFilter(field_name='date', label=['Date From', 'to'])
    start_date = filters.DateFilter(field_name='date', lookup_expr=('gt'), label='Date From', widget=forms.DateInput(attrs={'type': 'date', 'class': 'date-input'}))
    end_date = filters.DateFilter(field_name='date', lookup_expr=('lt'), label='to', widget=forms.DateInput(attrs={'type': 'date', 'class': 'date-input'}))

    class Meta:
        model = Order
        fields = ['order', 'billing_lastname', 'status_current', 'start_date', 'end_date']