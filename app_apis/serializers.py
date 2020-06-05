from rest_framework import serializers
from app_websites.models import *

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ('order_id', 'order_no', 'billing_name', 'billing_address_1', 'billing_address_2', 'billing_city', 'billing_postcode', 'billing_country', 'billing_email', 'billing_phone', 'delivery_name', 'delivery_address_1', 'delivery_address_2', 'delivery_city', 'delivery_postcode', 'delivery_country', 'delivery_email', 'delivery_phone', 'delivery_price', 'ip_address', 'website', 'date' )

class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('orderitem_id','order_id', 'product_id', 'item_price', 'item_qty', 'total_price')

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ('product_id', 'product_name', 'sku', 'sell_price', 'buy_price', 'stock_qty', 'weight', 'location', 'brand', 'supplier', 'url')

class SupplierSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Supplier
        fields = ('supplier')

class BrandSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Brand
        fields = ('brand')