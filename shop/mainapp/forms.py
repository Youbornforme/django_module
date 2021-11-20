from django import forms
from django.db import models

from .models import Order


class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_date'].label = 'Дата получения заказа'

    order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'phone', 'address', 'buying_type', 'order_date', 'comment'
        )


class RegisterForm(forms.Form):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(required=True, widget=forms.PasswordInput)

    def clean_password(self):
        if self.data['password'] != self.data['password2']:
            raise forms.ValidationError('Your password don\'t match.')
        return self.data['password']

    def clean_username(self):
        if models.User.objects.filter(username__iexact=self.data.get('username').lower()):
            raise forms.ValidationError('Username already taken.')
        return self.data['username']