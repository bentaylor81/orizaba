from django.urls import path
from . import views
from .views import *
from app_products.views import *
from app_orders.views import *
from django.conf import settings

urlpatterns = [   
    path('utils', views.utils, name='utils-list'),
    path('utils/orizaba-stock-reset', views.orizaba_stock_reset, name='orizaba-stock-reset'),   
    path('utils/current-stock-qty-null', views.current_stock_qty_null, name='current-stock-qty-null'), 
    path('utils/update-stock-descrepancy-stats', views.update_stock_descrepancy_stats, name='update-stock-descrepancy-stats'),      # Used in Stock List table in products 
    path('utils/update-stock-movement-date', views.update_stock_movement_date, name='update-stock-movement-date'),      # Update stock movement date date_added = order date
]
