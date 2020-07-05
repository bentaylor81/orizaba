from django.urls import path
from . import views

urlpatterns = [
    path('', views.orders, name="home"),
    path('orders/', views.orders, name="orders"),
    path('orders/<id>', views.order_view, name='order-view'),
    path('orders/view/update', views.order_view_update, name='order-view-update'),
]
