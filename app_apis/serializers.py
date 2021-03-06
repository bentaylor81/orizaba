from rest_framework import serializers
from app_products.models import *
from app_orders.models import *

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class ProductSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_id', 'sku', 'product_name']