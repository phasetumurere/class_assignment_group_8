from django import forms
from .models import *

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'phone', 'email', 'address_line1',
            'address_line2', 'country', 'district', 'sector', 'order_note',
        ]