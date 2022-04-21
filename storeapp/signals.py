from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from .models import Customer, Employee

def customer_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='customer')
        instance.groups.add(group)

        Customer.objects.create(
            user=instance,
            customer_First_Name=instance.first_name,
            customer_Last_Name=instance.last_name,
            customer_Email=instance.email,
        )

post_save.connect(customer_profile, sender=User)

''' def employee_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='employee')
        instance.groups.add(group)

        Employee.objects.create(
            user=instance,
            employee_First_Name=instance.first_name,
            employee_Last_Name=instance.last_name,
            employee_Email=instance.email,
            is_staff=True,
        )

post_save.connect(employee_profile, sender=User) '''