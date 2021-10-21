from django import forms
from . import models


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
        if models.MyUser.objects.filter(username__iexact=self.data.get('username').lower()):
            raise forms.ValidationError('Username already taken.')
        return self.data['username']

