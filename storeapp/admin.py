from django.contrib import admin

# Register your models here.

from .models import Customer, Employee, Vendor, Expediter, Material, Version, InputItem, Machine 
from .models import Job, Category, Product, Billing, Shipping, Order

admin.site.register(Customer)
admin.site.register(Employee)
admin.site.register(Vendor)
admin.site.register(Expediter)

admin.site.register(Material)
admin.site.register(Version)
admin.site.register(InputItem)
admin.site.register(Machine)
admin.site.register(Job)

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Billing)
admin.site.register(Shipping)
admin.site.register(Order)