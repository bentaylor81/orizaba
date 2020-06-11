from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('orders/', views.orders, name="orders"),
    path('orders/<id>', views.order_view, name='order-view'),
    path('products', views.products, name='products'),
    path('products/<id>', views.product_view, name='product-view'),
    path('suppliers', views.suppliers, name='suppliers'),
    path('suppliers/<path>', views.supplier_view, name='supplier-view'),
    path('customers', views.customers, name='customers'),
    path('customers/<path>', views.customer_view, name='customer-view'),
    path('brands', views.brands, name='brands'),
]
