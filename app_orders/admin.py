from django.contrib import admin
from .models import *

admin.site.register(Order)
admin.site.register(OrderNote)
admin.site.register(OrderItem)
admin.site.register(OrderStatusHistory)
admin.site.register(OrderStatusType)
admin.site.register(OrderDeliveryMethod)
admin.site.register(OrderShipment)
