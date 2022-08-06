from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from .models import Client, Portfolio, Security
from bootstrap_modal_forms.forms import BSModalModelForm

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        exclude = ['user']

class PortModalForm(ModelForm):
    class Meta:
        model = Portfolio
        fields = '__all__'
