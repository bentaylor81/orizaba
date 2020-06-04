from django.urls import path
from . import views

urlpatterns = [
   path('orders/', views.orders, name="orders"),
   path('orders/<id>', views.order_view, name='order-view'),
   path('products', views.products, name='products'),
   path('products/<id>', views.product_view, name='product-view'),
   path('suppliers', views.suppliers, name='suppliers'),
   path('brands', views.brands, name='brands'),
]
