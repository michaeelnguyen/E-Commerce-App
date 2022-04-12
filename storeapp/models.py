from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.functional import lazy
from django.utils.text import slugify




# Create your models here.

class Customer(models.Model):
    customer_First_Name = models.CharField(max_length=255, null=True)
    customer_Last_Name = models.CharField(max_length=255, null=True)
    customer_Phone_Number= models.CharField(max_length=255, null=True)
    customer_Email = models.EmailField(max_length=255, null=True)
    customer_Password= models.CharField(max_length=255, null=True)
    street_Address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, null=True)
    zip = models.CharField(max_length=255, null=True)

    slug = models.SlugField(max_length=255, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.customer_First_Name + " " + self.customer_Last_Name)
        super(Customer, self).save(*args, **kwargs)

    def __str__(self):
        return self.customer_First_Name + " " + self.customer_Last_Name


class Employee(models.Model):
    employee_First_Name = models.CharField(max_length=255, null=True)
    employee_Last_Name = models.CharField(max_length=255, null=True)
    employee_Phone_Number= models.CharField(max_length=255, null=True)
    employee_Email = models.EmailField(max_length=255, null=True)
    employee_Password= models.CharField(max_length=255, null=True)
    role = models.CharField(max_length=255, null=True)

    slug = models.SlugField(max_length=255, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.employee_First_Name + " " + self.employee_Last_Name)
        super(Employee, self).save(*args, **kwargs)

    def __str__(self):
        return self.employee_First_Name + " " + self.employee_Last_Name


class Vendor(models.Model):
    vendor_name = models.CharField(max_length=255, null=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.vendor_name


class Expediter(models.Model):
    expediter_name = models.CharField(max_length=255, null=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

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
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.material_Type


class Version(models.Model):
    product_Image = models.ImageField(upload_to='media/storeapp/product_images', null=True, blank=True)
    product_Version = models.CharField(max_length=255, null=True)
    product_Version_Date = models.DateTimeField(auto_now_add=False, null=True)
    product_Design_File = models.FileField(upload_to='media/storeapp/product_files', null=True)
    product_Comments = models.TextField(null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product_Version


class InputItem(models.Model):
    input_Name = models.CharField(max_length=255, null=True)
    quantity_Per_1000_Units = models.PositiveIntegerField(null=True)
    message_Commands = models.TextField(null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.input_Name


class Machine(models.Model):
    machine_Number = models.PositiveIntegerField(null=True)
    input_ID = models.ManyToManyField(InputItem, related_name='inputs')
    #input_ID = models.ForeignKey(InputItem, null=True, on_delete=models.SET_NULL)

    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['machine_Number']

    def __str__(self):
        return f' Machine #{self.machine_Number}'

class Job(models.Model):

    machine_ID = models.ForeignKey(Machine, null=True, on_delete=models.SET_NULL)
    employee = models.ForeignKey(Employee, null=True, on_delete=models.SET_NULL)
    start_Time = models.DateTimeField(auto_now_add=False, null=True)
    end_Time = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    quality_Comments = models.TextField(null=True, blank=True)
    defect_Count = models.PositiveIntegerField(null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['start_Time']

    def __str__(self):
        if self.end_Time == None:
            return f'[START TIME: {self.start_Time}] [END TIME: IN PROGRESS...]'
        return f'[START TIME: {self.start_Time}] [END TIME: {self.end_Time}]'


class Category(models.Model):
    category_Name = models.CharField(max_length=255, null=True)

    slug = models.SlugField(max_length=255, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Categories"
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_Name)
        super(Category, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.category_Name

class Product(models.Model):
    product_Name = models.CharField(max_length=255, null=True)
    product_Description = models.CharField(max_length=255, null=True)
    product_Price = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    product_Stock = models.BooleanField(default=True)
    
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    width = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    depth = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    category_ID = models.ForeignKey(Category, on_delete=models.RESTRICT)
    material_ID = models.ForeignKey(Material, null=False, on_delete=models.DO_NOTHING)
    version_ID = models.ForeignKey(Version, null=False, on_delete=models.DO_NOTHING)
    job_ID = models.ForeignKey(Job, null=True, on_delete=models.DO_NOTHING)
    
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.product_Name} --- DIMENSIONS ({self.height} x {self.width} x {self.width}) --- PRICE ${self.product_Price}'


class Billing(models.Model):
    #customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    billing_Address = models.CharField(max_length=255, null=True)
    billing_City = models.CharField(max_length=255, null=True)
    billing_State = models.CharField(max_length=255, null=True)
    billing_Zip = models.CharField(max_length=255, null=True)
    
    date_Billed = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    #card_Number =
    #expiration_Date = 
    #security_Code = 

    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Billing"
        ordering = ['date_Billed']
    
    def __str__(self):
        if self.date_Billed == None:
            return f'ADDRESS: {self.billing_Address}, {self.billing_City}, {self.billing_State}, {self.billing_Zip} -- DATE BILLED: NOT PROCESSED'
   
        return f'ADDRESS: {self.billing_Address}, {self.billing_City}, {self.billing_State}, {self.billing_Zip} -- DATE BILLED: {self.date_Billed.strftime("%d.%m.%Y")}'


class Shipping(models.Model):
    #customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
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
        return f'ADDRESS: {self.shipping_Address}, {self.shipping_City}, {self.shipping_State}, {self.shipping_Zip} -- DATE SHIPPED: {self.date_Shipped.strftime("%d.%m.%Y")}'


class Cart(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta: 
        ordering = ['customer']
    
    def __str__(self):
        return f'Cart Session ID #{self.id}'

#class OrderQuantity(models.Model):
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, null=True, on_delete=models.SET_NULL)
    product_id = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    item_quantity = models.PositiveIntegerField(null=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta: 
        ordering = ['product_id']

    def __str__(self):
        return f'{self.product_id}, Qty: {self.item_quantity}'


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
    )

    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)

    cart = models.ForeignKey(Cart, null=True, on_delete=models.SET_NULL)
    #product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    #order_quantity_ID = models.ForeignKey(OrderQuantity, null=True, on_delete=models.SET_NULL)

    order_Date = models.DateTimeField(auto_now_add=True, null=True)
    order_Status = models.CharField(max_length=255, null=True, choices=STATUS)
    confirmation_Number = models.CharField(max_length=255, null=True)
    billing_ID = models.ForeignKey(Billing, null=True, on_delete=models.SET_NULL)
    shipment_ID = models.ForeignKey(Shipping, null=True, on_delete=models.SET_NULL)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, null=True) 
    
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta: 
        ordering = ['order_Date']

    def __str__(self):
        return f'Order Number: {self.confirmation_Number} , Order Date: {self.order_Date.strftime("%d.%m.%Y")}, STATUS: {self.order_Status}'

