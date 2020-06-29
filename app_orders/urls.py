from django.urls import path
from . import views

urlpatterns = [
    path('', views.orders, name="home"),
    path('orders/', views.orders, name="orders"),
    path('orders/<id>', views.order_view, name='order-view'),
]
