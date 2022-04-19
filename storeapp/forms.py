from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Order, Customer, Product

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class CustomerRegistrationForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

