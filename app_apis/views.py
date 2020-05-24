from django.shortcuts import render
from rest_framework import viewsets

from .serializers import *
from app_websites.models import *


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-date')
    serializer_class = OrderSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all().order_by('-order_id')
    serializer_class = OrderItemSerializer

class OrderLineViewSet(viewsets.ModelViewSet):
    queryset = OrderLine.objects.all().order_by('-order_id')
    serializer_class = OrderItemSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-product_id')
    serializer_class = ProductSerializer
