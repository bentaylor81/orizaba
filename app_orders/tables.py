import django_tables2 as tables
from .models import Order

class OrderTable(tables.Table):
    class Meta:
        model = Order
        fields = ('date', 'order_no', 'delivery_name', 'delivery_address' )
        attrs = {"class": "django_tables", "cellpadding": 0, "cellspacing": 0 }