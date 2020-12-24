from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', OrderList.as_view(), name="home"),
    path('orders', OrderList.as_view(), name='order-list'),
    path('returns', ReturnList.as_view(), name='return-list'),
    path('refunds', RefundList.as_view(), name='refund-list'),
    path('orders/<pk>', OrderDetail.as_view(), name='order-detail'),
    path('orders/<id>/picklist', views.picklist_create, name='order-picklist'), 
    path('orders/<id>/invoice', views.invoice_create, name='order-invoice'), 
    path('orders/<id>/credit-note', views.credit_note_create, name='order-credit-note'), 
]

