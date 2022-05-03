import decimal
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Customer, InputItem, Job, Machine, Order, Product, Version

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name','last_name' , 'email', 'password1', 'password2']

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user', 'is_staff', 'slug', 'is_active']
        
class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class CustomProductForm(ModelForm):
    is_custom = forms.BooleanField(initial=True, disabled=True)
    
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['product_Price','product_Stock','job_ID', 'is_active']

class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = '__all__'

class VersionForm(ModelForm):
    class Meta:
        model = Version
        fields = '__all__'

class DateTimeInput(forms.DateTimeInput):
    input_type = 'date'

class CustomVersionForm(ModelForm):
    product_Version_Date = forms.DateTimeField(widget=DateTimeInput)

    class Meta:
        model = Version
        fields = ['product_Version', 'product_Version_Date' , 'product_Design_File']

class MachineForm(ModelForm):
    class Meta:
        model = Machine
        fields = '__all__'

class InputForm(ModelForm):
    class Meta:
        model = InputItem
        fields = '__all__'