from decimal import Decimal
import os
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    customer_First_Name = models.CharField(max_length=255, blank=True)
    customer_Last_Name = models.CharField(max_length=255, blank=True)
    customer_Phone_Number= models.CharField(max_length=255, blank=True)

    customer_Email = models.EmailField(max_length=255, blank=True)

    #street_Address = models.CharField(max_length=255, null=True)
    #city = models.CharField(max_length=255, null=True)
    #state = models.CharField(max_length=255, null=True)
    #zip = models.CharField(max_length=255, null=True)

    slug = models.SlugField(max_length=255, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    class Meta:
        ordering = ['customer_Last_Name']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user)
        super(Customer, self).save(*args, **kwargs)

    def __str__(self):
        return self.customer_First_Name + ' ' + self.customer_Last_Name


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    employee_First_Name = models.CharField(max_length=255, null=True)
    employee_Last_Name = models.CharField(max_length=255, null=True)
    employee_Phone_Number= models.CharField(max_length=255, null=True)
    employee_Email = models.EmailField(max_length=255, null=True)

    role = models.CharField(max_length=255, null=True)

    slug = models.SlugField(max_length=255, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    class Meta:
        ordering = ['employee_Last_Name']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.employee_First_Name + " " + self.employee_Last_Name)
        super(Employee, self).save(*args, **kwargs)

    def __str__(self):
        return self.employee_First_Name + " " + self.employee_Last_Name


class Vendor(models.Model):
    vendor_name = models.CharField(max_length=255, null=True)

    slug = models.SlugField(max_length=255, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['vendor_name']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.vendor_name)
        super(Vendor, self).save(*args, **kwargs)

    def __str__(self):
        return self.vendor_name


class Expediter(models.Model):
    expediter_name = models.CharField(max_length=255, null=True)

    slug = models.SlugField(max_length=255, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['expediter_name']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.expediter_name)
        super(Expediter, self).save(*args, **kwargs)

    def __str__(self):
        return self.expediter_name


class Material(models.Model):
    MATERIAL_TYPES = (
        ('Acrylic/Polymethyl Methacrylate (PMMA)', 'Acrylic/Polymethyl Methacrylate (PMMA)'),
        ('Polycarbonate (PC)', 'Polycarbonate (PC)'),
        ('Polyethlene (PE)', 'Polyethlene (PE)'),
        ('Polypropylene (PP)', 'Polypropylene(PP)'),
        ('Polyethylene Terephthalate (PET)', 'Polyethylene Terephthalate (PET)'),
        ('Polyvinyl Chloride (PVC)', 'Polyvinyl Chloride (PVC)'),
        ('Acrylonitrile-Butadiene-Stryrene (ABS)', 'Acrylonitrile-Butadiene-Stryrene (ABS)'),
    )

    material_Type = models.CharField(max_length=255, null=True)#, choices=MATERIAL_TYPES)
    
    slug = models.SlugField(max_length=255, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['material_Type']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.material_Type)
        super(Material, self).save(*args, **kwargs)

    def __str__(self):
        return self.material_Type


class Version(models.Model):
    #product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    
    product_Image = models.ImageField(upload_to='media/storeapp/product_images', null=True, blank=True)
    product_Version = models.CharField(max_length=255, null=True, blank=True)
    product_Version_Date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    product_Design_File = models.FileField(upload_to='media/storeapp/product_files', null=True, blank=True)
    product_Comments = models.TextField(null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['product_Version']

    def __str__(self):
        if self.customer is None:
            return f'{self.product_Version}'
        else:
            return f'{self.product_Version}'
    
    def filename(self):
        return os.path.basename(self.product_Design_File.path)


class InputItem(models.Model):
    input_Name = models.CharField(max_length=255, null=True)
    quantity_Per_1000_Units = models.PositiveIntegerField(null=True)
    message_Commands = models.TextField(null=True, blank=True)
    vendor = models.ForeignKey(Vendor, null=True, on_delete=models.SET_NULL)
    
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-input_Name']

    def __str__(self):
        return f'{self.input_Name} / QTY: {self.quantity_Per_1000_Units}'

class Machine(models.Model):
    #job = models.ForeignKey(Job, null=True, on_delete=models.SET_NULL, blank=True)
    machine_Number = models.PositiveIntegerField(null=True)
    input = models.ManyToManyField(InputItem, related_name='inputs')
    
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['machine_Number']

    def __str__(self):
        return f' Machine #{self.machine_Number}'

class Job(models.Model):
    machine_ID = models.ForeignKey(Machine, null=True, on_delete=models.SET_NULL, blank=True)
    employee = models.ForeignKey(Employee, null=True, on_delete=models.SET_NULL)
    start_Time = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    end_Time = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    quality_Comments = models.TextField(null=True, blank=True)
    defect_Count = models.PositiveIntegerField(null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-start_Time']

    def __str__(self):
        if self.end_Time == None:
            return f'{self.employee} - [START TIME: {self.start_Time}] [END TIME: IN PROGRESS...]'
        return f'{self.employee} - [START TIME: {self.start_Time.strftime("%m/%d/%Y, %H:%M")}] [END TIME: {self.end_Time.strftime("%m/%d/%Y, %H:%M")}]'

class Category(models.Model):
    category_Name = models.CharField(max_length=255, null=True)

    slug = models.SlugField(max_length=255, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['category_Name']
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_Name)
        super(Category, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.category_Name


class Product(models.Model):
    product_Name = models.CharField(max_length=255, null=True)
    product_Description = models.CharField(max_length=255, null=True)
    product_Price = models.DecimalField(max_digits=12, decimal_places=2, null=True, default=Decimal('0.00'))
    product_Stock = models.BooleanField(default=True)
    
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    width = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    depth = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    category_ID = models.ForeignKey(Category, on_delete=models.RESTRICT)
    material_ID = models.ForeignKey(Material, null=True, on_delete=models.DO_NOTHING)
    version_ID = models.ForeignKey(Version, related_name='versionList', null=True, on_delete=models.DO_NOTHING, blank=True)
    job_ID = models.ForeignKey(Job, null=True, on_delete=models.DO_NOTHING, blank=True)
    
    is_custom = models.BooleanField(default=False)
    
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['product_Name']

    def __str__(self):
        return f'{self.product_Name}'
    
    @property
    def imageURL(self):
        try:
            url = self.version_ID.product_Image.url
        except:
            url = ''
        return url

class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    #product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)

    order_Date = models.DateTimeField(auto_now_add=True, null=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    order_Status = models.CharField(max_length=255, null=True, blank=True, choices=STATUS)
    confirmation_Number = models.CharField(max_length=255, null=True)
    
    total = models.DecimalField(max_digits=12, decimal_places=2, null=True) 
    
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta: 
        ordering = ['order_Date']
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    def __str__(self):
        return f'Order Number: {self.confirmation_Number}, Order Date: {self.order_Date.strftime("%d.%m.%Y")}, Customer: {self.customer}'



class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.product_Price * self.quantity
        return total
    
    def __str__(self):
        return f'{self.product.product_Name}'


class Billing(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    
    billing_Address = models.CharField(max_length=255, null=True)
    billing_City = models.CharField(max_length=255, null=True)
    billing_State = models.CharField(max_length=255, null=True)
    billing_Zip = models.CharField(max_length=255, null=True)
    
    date_Billed = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Billing"
        ordering = ['date_Billed']
    
    def __str__(self):
        if self.date_Billed == None:
            return f'{self.billing_Address}, {self.billing_City}, {self.billing_State}, {self.billing_Zip} -- DATE BILLED: NOT PROCESSED'
   
        return f'{self.billing_Address}, {self.billing_City}, {self.billing_State}, {self.billing_Zip} -- DATE BILLED: {self.date_Billed.strftime("%d.%m.%Y")}'


class Shipping(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    
    shipping_Address = models.CharField(max_length=255, null=True)
    shipping_City = models.CharField(max_length=255, null=True)
    shipping_State = models.CharField(max_length=255, null=True)
    shipping_Zip = models.CharField(max_length=255, null=True)
    
    date_Shipped = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    expediter_ID = models.ForeignKey(Expediter, null=True, on_delete=models.SET_NULL)
    shipment_Cost = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    shipment_Quantity = models.PositiveIntegerField(null=True)
    shipment_Weight = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Shipping"
        ordering = ['date_Shipped']
    
    def __str__(self):
        if self.date_Shipped == None:
            return f'{self.shipping_Address}, {self.shipping_City}, {self.shipping_State}, {self.shipping_Zip} -- DATE BILLED: NOT PROCESSED'
   
        return f'{self.shipping_Address}, {self.shipping_City}, {self.shipping_State}, {self.shipping_Zip} -- DATE BILLED: {self.date_Shipped.strftime("%d.%m.%Y")}'