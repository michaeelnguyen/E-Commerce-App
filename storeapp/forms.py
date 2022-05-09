from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Billing, Category, Customer, Expediter, InputItem, Job, Machine, Material, Order, OrderItem, Product, Shipping, Version

STATUS = (
    ('Pending', 'Pending'),
    ('Shipped', 'Shipped'),
    ('Out for Delivery', 'Out for Delivery'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),
)

class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime'



class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class EditOrderForm(ModelForm):
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), disabled=True)
    confirmation_Number = forms.CharField(disabled=True)
    order_Status = forms.ChoiceField(choices=STATUS)
    
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['complete', 'total']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name','last_name' , 'email', 'password1', 'password2']

class CustomerForm(ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), disabled=True, label='Username')
    customer_First_Name = forms.CharField(disabled=True, label='First Name')
    customer_Last_Name = forms.CharField(disabled=True, label='Last Name')
    customer_Email = forms.CharField(label='Email')
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['is_staff', 'slug']
        
class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class CustomProductForm(ModelForm):
    is_custom = forms.BooleanField(initial=True, disabled=True)
    category_ID = forms.ModelChoiceField(queryset=Category.objects.all(), label="Category")
    material_ID = forms.ModelChoiceField(queryset=Material.objects.all(), label="Material Type")
    version_ID = forms.ModelChoiceField(queryset=Version.objects.all(), label="Version")
    
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['product_Price','product_Stock','job_ID', 'is_active']

class JobForm(ModelForm):
    start_Time = forms.DateTimeField(widget=DateTimeInput)
    end_Time = forms.DateTimeField(widget=DateTimeInput)
    class Meta:
        model = Job
        fields = '__all__'

class VersionForm(ModelForm):
    class Meta:
        model = Version
        fields = '__all__'

class CustomVersionForm(ModelForm):
    product_Version_Date = forms.DateTimeField(widget=DateTimeInput, label='Version Date')
    
    class Meta:
        model = Version
        fields = ['customer','product_Version', 'product_Version_Date' , 'product_Design_File']

class EditVersionForm(ModelForm):
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), disabled=True)
    product_Version_Date = forms.DateTimeField(widget=DateTimeInput, label='Version Date')

    class Meta:
        model = Version
        fields = ['customer','product_Version', 'product_Version_Date' , 'product_Design_File']
        
class MachineForm(ModelForm):
    class Meta:
        model = Machine
        fields = '__all__'

class InputForm(ModelForm):
    class Meta:
        model = InputItem
        fields = '__all__'

class OrderItemForm(ModelForm):
    quantity = forms.IntegerField(min_value=1)
    product = forms.ModelChoiceField(queryset=Product.objects.all(), disabled=True)
    class Meta:
        model = OrderItem
        fields = '__all__'
        exclude = ['order']

class ViewOrderForm(ModelForm):
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), disabled=True)
    confirmation_Number = forms.CharField(disabled=True, label='Confirmation #')
    order_Status = forms.ChoiceField(choices=STATUS, disabled=True, label='Order Status')
    total = forms.DecimalField(disabled=True)

    class Meta:
        model = Order
        fields = ['customer', 'order_Status', 'confirmation_Number', 'total']
        exclude = ['complete', 'is_active']

class ViewOrderItemForm(ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), disabled=True)
    quantity = forms.IntegerField(min_value=1, disabled=True)
    class Meta:
        model = OrderItem
        fields = '__all__'
        exclude = ['order']

class BillingForm(ModelForm):
    billing_Address = forms.CharField(disabled=True, label='Billing Address')
    billing_City = forms.CharField(disabled=True, label='City')
    billing_State = forms.CharField(disabled=True, label='State')
    billing_Zip = forms.CharField(disabled=True, label='Zip Code')

    date_Billed = forms.DateTimeField(widget=DateTimeInput, disabled=True, label='Date Billed')

    class Meta: 
        model = Billing
        fields = '__all__'
        exclude = ['customer', 'order', 'is_active']

class ShippingForm(ModelForm):
    shipping_Address = forms.CharField(disabled=True, label='Shipping Address')
    shipping_City = forms.CharField(disabled=True, label='City')
    shipping_State = forms.CharField(disabled=True, label='State')
    shipping_Zip = forms.CharField(disabled=True, label='Zip Code')

    #shipment_Cost = forms.DecimalField(disabled=True, label='Shipping Cost')
    #shipment_Quantity = forms.IntegerField(disabled=True, label='Shipping Quantity')
    shipment_Weight = forms.DecimalField(disabled=True, label='Shipping Weight')

    date_Shipped = forms.DateTimeField(widget=DateTimeInput, disabled=True, label="Date Shipped")

    expediter_ID = forms.ModelChoiceField(queryset=Expediter.objects.all(), disabled=True, label='Expediter')
    class Meta:
        model = Shipping
        fields = '__all__'
        exclude = ['customer', 'order', 'is_active', 'shipment_Cost', 'shipment_Quantity']