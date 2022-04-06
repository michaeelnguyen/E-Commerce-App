from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.functional import lazy





# Create your models here.

class Customer(models.Model):
    customer_First_Name = models.CharField(max_length=30, null=True)
    customer_Last_Name = models.CharField(max_length=30, null=True)
    customer_Phone_Number= models.CharField(max_length=30, null=True)
    customer_Email = models.EmailField(max_length=30, null=True)
    customer_Password= models.CharField(max_length=30, null=True)
    street_Address = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=30, null=True)
    state = models.CharField(max_length=30, null=True)
    zip = models.CharField(max_length=30, null=True)

    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_First_Name + " " + self.customer_Last_Name





class Employee(models.Model):
    employee_First_Name = models.CharField(max_length=30, null=True)
    employee_Last_Name = models.CharField(max_length=30, null=True)
    employee_Phone_Number= models.CharField(max_length=30, null=True)
    employee_Email = models.EmailField(max_length=30, null=True)
    employee_Password= models.CharField(max_length=30, null=True)
    role = models.CharField(max_length=30, null=True)

    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.employee_First_Name + " " + self.employee_Last_Name






class Vendor(models.Model):
    VENDORS = (
        ('Dow Chemical', 'Dow Chemical'),
        ('ExxonMobil', 'ExxonMobil'),
        ('Adapt Plastics, Inc', 'Adapt Plastics, Inc'),
        ('A&S Mold & Die Corp', 'A&S Mold & Die Corp'),
    )
    vendor_Name = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.vendor_Name






class Expediter(models.Model):
    
    EXPEDITERS = (
        ('Amazon', 'Amazon'),
        ('FedEx', 'FedEx'),
        ('UPS', 'UPS'),
        ('OnTrac', 'OnTrac'),
    )
    expeditor_Name = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.expeditor_Name






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
    material_Type = models.CharField(max_length=50, null=True, choices=MATERIAL_TYPES)

    def __str__(self):
        return self.material_Type






class Product(models.Model):
    product_Name = models.CharField(max_length=30, null=True)
    product_Description = models.CharField(max_length=50, null=True)
    product_Price = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    product_Stock = models.PositiveIntegerField(null=True)
    
    material_Type = models.ForeignKey(Material, null=True, on_delete=models.SET_NULL)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    width = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    depth = models.DecimalField(max_digits=5, decimal_places=2, null=True)
   
    product_Image = models.ImageField(upload_to='media/storeapp/product_images', null=True, blank=True)
    product_Version = models.CharField(max_length=10, null=True)
    product_Version_Date = models.DateTimeField(auto_now_add=False, null=True)
    product_Design_File = models.FileField(upload_to='media/storeapp/product_files', null=True, blank=True)
    product_Comments = models.TextField(null=True, blank=True)
    
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_Name






class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
    )
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    order_Date = models.DateTimeField(auto_now_add=True, null=True)
    vendor = models.ForeignKey(Vendor, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=20, null=True, choices=STATUS)