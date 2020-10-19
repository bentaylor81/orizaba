from django.urls import path
from . import views
from .views import *
from django.conf import settings

urlpatterns = [   
    path('utils', views.utils, name='utils-list'),
    path('utils/orizaba-stock-reset', views.orizaba_stock_reset, name='orizaba-stock-reset'),   
    path('utils/current-stock-qty-null', views.current_stock_qty_null, name='current-stock-qty-null'),      
]
