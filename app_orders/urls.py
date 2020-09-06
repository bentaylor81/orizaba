from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', OrderList.as_view(), name="home"),
    path('orders', OrderList.as_view(), name='order-list'),
    path('orders/<pk>', OrderDetail.as_view(), name='order-detail'),
    path('orders/<pk>/picklist/edit', OrderPicklistEdit.as_view(), name='order-picklist-edit'), 
    path('orders/<id>/picklist', views.picklist_create, name='order-picklist'), 
    path('orders/<id>/invoice', views.invoice_create, name='order-invoice'), 
]
