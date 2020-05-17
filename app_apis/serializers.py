from rest_framework import serializers
from app_websites.models import Order

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'url', 'order_no', 'name', 'address_1', 'address_2', 'city', 'postcode', 'country', 'phone', 'date' )