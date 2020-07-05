from django import forms
from .models import *

class OrderNoteForm(forms.ModelForm):
    class Meta:
        model = OrderNote
        fields = ["note", "order_id", "added_by"]

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ["orderitem_id", "order_id", "send_qty", "active"]