from django.contrib import admin
from .models import *

admin.site.register(Order)
admin.site.register(OrderNote)
admin.site.register(OrderItem)
admin.site.register(Product)
admin.site.register(Supplier)
admin.site.register(Brand)
