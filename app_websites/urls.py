from django.urls import path
from . import views
from .views import ProductListView, SupplierListView

urlpatterns = [

    
    path('products', ProductListView.as_view(), name='products'),
    path('suppliers', SupplierListView.as_view(), name='suppliers'),

    path('products/<id>', views.product_view, name='product-view'),

    path('suppliers/<path>', views.supplier_view, name='supplier-view'),
    path('customers', views.customers, name='customers'),
    path('customers/<path>', views.customer_view, name='customer-view'),
    path('brands', views.brands, name='brands'),
]
