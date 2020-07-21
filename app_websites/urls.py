from django.urls import path
from . import views
from .views import *


urlpatterns = [   
    path('products', ProductListView.as_view(), name='products'),
    path('product/label/<id>', views.generate_label, name='product-label'),

    path('products/<id>', views.product_view, name='product-view'),
    path('suppliers', SupplierListView.as_view(), name='suppliers'),

    path('suppliers/<path>', views.supplier_view, name='supplier-view'),
    path('customers', views.customers, name='customers'),
    path('customers/<path>', views.customer_view, name='customer-view'),
    path('brands', views.brands, name='brands'),
]

