from django.contrib import admin
from app_products.models import *
from app_orders.models import *

admin.site.register(Order)
admin.site.register(OrderNote)
admin.site.register(OrderItem)
admin.site.register(OrderStatusHistory)
admin.site.register(OrderStatusType)
admin.site.register(OrderDeliveryMethod)
admin.site.register(Product)
admin.site.register(Supplier)
admin.site.register(Brand)
admin.site.register(Customer)

