from django import forms
from .models import *
from django.forms import inlineformset_factory

class OrderDeliveryDetailsForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["delivery_name", "delivery_address_1", "delivery_address_2", "delivery_city", "delivery_postcode", "delivery_country", "delivery_phone", "delivery_email", "delivery_method", "date_sent"]

class OrderShipmentForm(forms.ModelForm):
    class Meta:
        model = OrderShipment
        fields = ["delivery_name", "delivery_address_1", "delivery_address_2", "delivery_city", "delivery_postcode", "delivery_country", "delivery_phone", "delivery_email", "delivery_method", "date_sent" ]

class OrderNoteForm(forms.ModelForm):
    class Meta:
        model = OrderNote
        fields = ["note"]

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = []

OrderItemFormset = inlineformset_factory(
    Order, 
    OrderItem, 
    extra=0, 
    can_delete=False,
    fields=('order_id', 'item_qty', 'send_qty', 'product_id' ),
    widgets={
        'send_qty' : forms.NumberInput(attrs={'class':'send_qty', 'min': '0' }), 
        'product_id' : forms.TextInput(attrs={'type': 'hidden'})
        }
    )
