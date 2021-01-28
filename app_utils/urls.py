from django.urls import path
from . import views
from .views import *
from app_products.views import *
from app_orders.views import *
from app_utils.views import *
from django.conf import settings

urlpatterns = [    
    # INDIVIDUAL PAGES 
    path('utils/stock-reconcile', StockMovementList.as_view(), name='stock-reconcile'),
    path('utils/stock-sync', StockSync.as_view(), name='stock-sync'),  
    path('utils/api-log-list', ApiLogList.as_view(), name='api-log-list'),  
    path('utils/magento-product-sync', MagentoProductSync.as_view(), name='magento-product-sync'),  
    # SEPARATE FUNCTIONS
    path('utils', views.utils, name='utils-list'),
    path('utils/orizaba-stock-reset', views.orizaba_stock_reset, name='orizaba-stock-reset'),   
    path('utils/current-stock-qty-null', views.current_stock_qty_null, name='current-stock-qty-null'), 
    path('utils/update-stock-descrepancy-stats', views.update_stock_descrepancy_stats, name='update-stock-descrepancy-stats'),      # Used in Stock List table in products 
    path('utils/update-stock-movement-date', views.update_stock_movement_date, name='update-stock-movement-date'),      # Update stock movement date date_added = order date
    path('utils/set-firstname-lastname', views.set_firstname_lastname, name='set-firstname-lastname'),      # Set the firstname and lastname for billing and delivery address
    path('utils/shiptheory-token', views.shiptheory_token, name='shiptheory-token'),  
    path('utils/shiptheory-tracking-code', views.shiptheory_tracking_code, name='shiptheory-tracking-code'),  
    path('utils/xero-token', views.xero_token, name='xero-token'),
    path('utils/redis-creds', views.redis_creds, name='redis-creds'),    
    # GENERAL SCRIPTS - RUN FUNCTIONS WHICH ARE USED ONCE
    path('utils/scripts', views.scripts, name='scripts'),   
]
