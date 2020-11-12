from django.urls import path
from . import views
from .views import *
from app_products.views import *
from app_orders.views import *
from django.conf import settings

urlpatterns = [    
    # INDIVIDUAL PAGES 
    path('utils/stock-reconcile', StockMovementList.as_view(), name='stock-reconcile'),
    path('utils/stock-sync', StockSync.as_view(), name='stock-sync'),  
    # SEPARATE FUNCTIONS
    path('utils', views.utils, name='utils-list'),
    path('utils/orizaba-stock-reset', views.orizaba_stock_reset, name='orizaba-stock-reset'),   
    path('utils/current-stock-qty-null', views.current_stock_qty_null, name='current-stock-qty-null'), 
    path('utils/update-stock-descrepancy-stats', views.update_stock_descrepancy_stats, name='update-stock-descrepancy-stats'),      # Used in Stock List table in products 
    path('utils/set-firstname-lastname', views.set_firstname_lastname, name='set-firstname-last'),      # Set the firstname and lastname for billing and delivery address
    ]
