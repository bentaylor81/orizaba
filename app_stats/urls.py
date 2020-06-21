from django.urls import path
from . import views

app_name = 'app_stats'
urlpatterns = [
    path('stats/sales/daily', views.stats_sales_day, name="stats-sal-day"),
    path('stats/sales/monthly', views.stats_sales_mon, name="stats-sal-mon"),
    path('stats/sales/yearly', views.stats_sales_year, name="stats-sal-year"),
    path('stats/products/financial-view', views.stats_prod_fin, name="stats-pro-fin"),
    path('stats/products/stock-view', views.stats_prod_sto, name="stats-pro-sto"),
    path('stats/brands', views.stats_brands, name="stats-brands"),
    path('stats/suppliers', views.stats_suppliers, name="stats-suppliers"),
    path('stats/customers', views.stats_customers, name="stats-customers"),
]