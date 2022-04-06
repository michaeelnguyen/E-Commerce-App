from django.contrib import admin

# Register your models here.

from .models import Customer, Employee, Product, Order, Vendor, Expediter, Material

admin.site.register(Customer)
admin.site.register(Employee)
admin.site.register(Vendor)
admin.site.register(Expediter)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Material)
