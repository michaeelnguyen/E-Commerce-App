import random
from tkinter import E
from django.core.management.base import BaseCommand
from faker import Faker
from faker.providers import BaseProvider
from storeapp.models import Category, Customer, Employee, Product, Material, Vendor, Expediter, Version, InputItem

import datetime
from django.conf import settings
from django.utils.timezone import make_aware

# POSSIBLE CATEGORIES?
CATEGORIES = [
    "Sheets",
    "Rods",
    "Tubing",
    "Films",
    "Parts",
    "Bottles",
    "Containers",
    "Packaging",
]

PRODUCTS = [
    "Sheets",
    "Rods",
    "Tubing",
    "Films",
    "Parts",
    "Bottles",
    "Containers",
    "Packaging",
]

VENDORS = [
    "Dow Chemical",
    "ExxonMobil",
    "Adapt Plastics, Inc",
    "A&S Mold & Die Corp",
]

EXPEDITERS = [
    "Amazon",
    "FedEx",
    "UPS",
    "OnTrac",
]

MATERIAL_TYPES = [
    "Acrylic/Polymethyl Methacrylate (PMMA)",
    "Polycarbonate (PC)",
    "Polyethlene (PE)",
    "Polypropylene (PP)",
    "Polyethylene Terephthalate (PET)",
    "Polyvinyl Chloride (PVC)",
    "Acrylonitrile-Butadiene-Stryrene (ABS)",
]

INPUT_ITEMS = [
    "Plastic Pellets",
    "COLOR - CYAN",
    "COLOR - MAGENTA",
    "COLOR - YELLOW",
    "COLOR - BLACK",
]

    

class Provider(BaseProvider):
    def ecommerce_category(self):
        return self.random_element(CATEGORIES)

    def ecommerce_product(self):
        return self.random_element(PRODUCTS)     

    def ecommerce_vendor(self):
        return self.random_element(VENDORS)

    def ecommerce_expediter(self):
        return self.random_element(EXPEDITERS)

    def ecommerce_material(self):
        return self.random_element(MATERIAL_TYPES)
    
    def ecommerce_inputItem(self):
        return self.random_element(INPUT_ITEMS)

class Command(BaseCommand):
    help = "Command Infomation"

    def handle(self, *args, **kwargs):
        
        fake = Faker(["en"])
        fake.add_provider(Provider)

        # Amount of Fake Records created
        numRecords = 15
        '''
        for _ in range(len(CATEGORIES) ):
            c = fake.unique.ecommerce_category()
            Category.objects.create(category_Name=c, slug=c)
        
        for _ in range(len(VENDORS)):
            v = fake.unique.ecommerce_vendor()
            Vendor.objects.create(vendor_Name=v, slug=v)
        
        for _ in range(len(EXPEDITERS)):
            e = fake.unique.ecommerce_expediter()
            Expediter.objects.create(expediter_Name=e, slug=e)
        
        for _ in range(len(MATERIAL_TYPES)):
            m = fake.unique.ecommerce_material()
            Material.objects.create(material_Type=m)
            
        for _ in range(len(INPUT_ITEMS)):
            i = fake.unique.ecommerce_inputItem()
            InputItem.objects.create(input_Name=i, slug=i)
        # Customer
        for _ in range(numRecords):
            fn = fake.first_name()
            ln = fake.last_name()
            pn = fake.unique.phone_number()
            email = fake.ascii_email()
            pw = fake.password(length=12)
            addr = fake.street_address()
            c = fake.city()
            st = fake.administrative_unit()
            z = fake.postcode()
            s = fn + "-" + ln

            Customer.objects.create(
                customer_First_Name = fn,
                customer_Last_Name = ln,
                customer_Phone_Number = pn,
                customer_Email = email,
                customer_Password = pw,
                street_Address = addr,
                city = c,
                state = st,
                zip = z,
                slug = s
                )
        

        # Employee
        for _ in range(numRecords):
            fn = fake.first_name()
            ln = fake.last_name()
            pn = fake.unique.phone_number()
            email = fake.ascii_company_email()
            pw = fake.password(length=12)
            r = fake.job()
            s = fn + "-" + ln

            Employee.objects.create(
                employee_First_Name = fn,
                employee_Last_Name = ln,
                employee_Phone_Number = pn,
                employee_Email = email,
                employee_Password = pw,
                role = r,
                slug = s
                )
        

        # Version
        for _ in range(numRecords):
            p_image = fake.file_name(category='image')
            p_version = round(random.uniform(00.01, 99.99),2)
            p_version_date = fake.date_time_this_decade()
            p_design_file = fake.file_name(extension='cad')
            p_comments = fake.paragraph()

            Version.objects.create(
                product_Image = p_image,
                product_Version = p_version,
                product_Version_Date = p_version_date,
                product_Design_File = p_design_file,
                product_Comments = p_comments,
            )
            '''



            #check_category = Category.objects.all().count()
            #self.stdout.write(self.style.SUCCESS(f'Number of categories: {check_category}'))