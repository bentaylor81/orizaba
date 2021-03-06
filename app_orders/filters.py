from django import forms
from django_filters import rest_framework as filters
from .models import *

class OrderFilter(filters.FilterSet):

    STATUS_CHOICES = [
        (10, 'Order Received'),
        (20, 'Shipment Created'),
        (40, 'Order Delivered'),
    ]

    order = filters.CharFilter(field_name='order_no', label='Order Number', lookup_expr='icontains')
    billing_lastname = filters.CharFilter(field_name='billing_lastname', label='Billing Surname', lookup_expr='icontains')       
    order_status = filters.ChoiceFilter(field_name='status_current', label='Order Status', choices=STATUS_CHOICES)  
    start_date = filters.DateFilter(field_name='date', lookup_expr=('gt'), label='Date From', widget=forms.DateInput(attrs={'type': 'date', 'class': 'date-input', 'id':'dateFromInput'}))
    end_date = filters.DateFilter(field_name='date', lookup_expr=('lt'), label='to', widget=forms.DateInput(attrs={'type': 'date', 'class': 'date-input', 'id':'dateToInput'}))

    class Meta:
        model = Order
        fields = ['order', 'billing_lastname', 'order_status', 'start_date', 'end_date']

class RefundFilter(filters.FilterSet):

    order = filters.CharFilter(field_name='order_id__order_no', label='Order Number', lookup_expr='icontains')
    billing_lastname = filters.CharFilter(field_name='billing_lastname', label='Billing Surname', lookup_expr='icontains')   

    class Meta:
        model = RefundOrder
        fields = ['order', 'billing_lastname']

class ReturnFilter(filters.FilterSet):

    order = filters.CharFilter(field_name='order_no', label='Order Number', lookup_expr='icontains')
    billing_lastname = filters.CharFilter(field_name='billing_lastname', label='Billing Surname', lookup_expr='icontains')   

    class Meta:
        model = RefundOrder
        fields = ['order', 'billing_lastname']
        