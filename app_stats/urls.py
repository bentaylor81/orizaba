from django.urls import path
from . import views

app_name = 'app_stats'
urlpatterns = [
    path('stats/sales', views.stats_sales, name="stats-sales"),
    path('stats/products', views.stats_products, name="stats-products"),
    path('stats/brands', views.stats_brands, name="stats-brands"),
    path('stats/suppliers', views.stats_suppliers, name="stats-suppliers"),
    path('stats/customers', views.stats_customers, name="stats-customers"),
]