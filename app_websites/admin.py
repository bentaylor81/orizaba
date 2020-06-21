from django.contrib import admin
from app_websites.models import *
from app_stats.models import *

admin.site.register(Order)
admin.site.register(OrderNote)
admin.site.register(OrderItem)
admin.site.register(Product)
admin.site.register(Supplier)
admin.site.register(Brand)
admin.site.register(Customer)
admin.site.register(Year)
admin.site.register(Month)
admin.site.register(Day)

