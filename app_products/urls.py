from django.urls import path
from . import views
from .views import *

urlpatterns = [   
    path('products', ProductList.as_view(), name='products'),
    path('products/<id>', views.product_view, name='product-view'),
    path('product/label/<id>', views.generate_label, name='product-label'),
    
    path('suppliers', SupplierList.as_view(), name='suppliers'),
    path('suppliers/<path>', views.supplier_view, name='supplier-view'),
    path('customers', views.customers, name='customers'),
    path('customers/<path>', views.customer_view, name='customer-view'),
    path('brands', views.brands, name='brands'),
]

