from django.urls import path
from . import views
from .views import *

urlpatterns = [   
    path('products', ProductList.as_view(), name='product-list'),
    path('purchase-orders', PurchaseOrderList.as_view(), name='purchase-order-list'),
    path('purchase-orders/<pk>', PurchaseOrderDetail.as_view(), name='purchase-order-detail'),
    path('suppliers', SupplierList.as_view(), name='supplier-list'),
    path('customers', CustomerList.as_view(), name='customer-list'),
    path('brands', BrandList.as_view(), name='brand-list'),

    path('products/<id>', views.product_view, name='product-detail'),
    path('suppliers/<path>', views.supplier_view, name='supplier-detail'), 
    path('customers/<path>', views.customer_view, name='customer-detail'),

    path('product/label/<id>', views.generate_label, name='product-label'), 
]


