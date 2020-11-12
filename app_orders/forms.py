from django import forms
from .models import *
from django.forms import inlineformset_factory

class OrderDeliveryDetailsForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["delivery_name", "delivery_firstname", "delivery_lastname", "delivery_address_1", "delivery_address_2", "delivery_city", "delivery_postcode", "delivery_country", "delivery_phone", "delivery_email"]

class OrderShipmentForm(forms.ModelForm):
    picklist = forms.BooleanField(required=False)
    class Meta:
        model = OrderShipment
        fields = ["delivery_firstname", "delivery_lastname", "delivery_address_1", "delivery_address_2", "delivery_city", "delivery_postcode", "delivery_country", "delivery_phone", "delivery_email", "total_price_ex_vat", "weight", "date_sent", "shipping_ref", "service_id", "picklist"]

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

class EmailInvoiceForm(forms.Form):
    to_email = forms.EmailField(max_length=254) 
    subject = forms.CharField(max_length=200)
    message = forms.CharField()

