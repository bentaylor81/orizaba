from django.shortcuts import render
from rest_framework import viewsets

from .serializers import OrderSerializer
from app_websites.models import Order


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-date')
    serializer_class = OrderSerializer
