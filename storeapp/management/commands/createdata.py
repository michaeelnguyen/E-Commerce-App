import random
from django.core.management.base import BaseCommand
from faker import Faker
from faker.providers import BaseProvider
from storeapp.models import Category, Customer, Employee, Machine, Product, Material, Vendor, Expediter, Version, InputItem, Billing, Shipping, Job, Order
from django.contrib.auth.models import User

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

STATUS = [
    "Pending",
    "Shipped",
    "Out for Delivery",
    "Delivered",
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
    
    def ecommerce_status(self):
        return self.random_element(STATUS)

class Command(BaseCommand):
    help = "Command Infomation"

    def handle(self, *args, **kwargs):
        
        fake = Faker(["en"])
        fake.add_provider(Provider)

        # Amount of Fake Records created
        numRecords = 15
        '''
        for _ in range(len(INPUT_ITEMS)):
            i = fake.unique.ecommerce_inputItem()
            InputItem.objects.create(input_Name=i)

        for _ in range(len(VENDORS)):
            v = fake.unique.ecommerce_vendor()
            Vendor.objects.create(vendor_name=v, slug=v)
        
        for _ in range(len(EXPEDITERS)):
            e = fake.unique.ecommerce_expediter()
            Expediter.objects.create(expediter_name=e, slug=e)

        for _ in range(len(CATEGORIES) ):
            c = fake.unique.ecommerce_category()
            Category.objects.create(category_Name=c, slug=c)
        
        for _ in range(len(MATERIAL_TYPES)):
            m = fake.unique.ecommerce_material()
            Material.objects.create(material_Type=m, slug=m)
        
        # Users
        for _ in range(numRecords):
            fn = fake.first_name()
            ln = fake.last_name()

            un = fn + ln + str(random.randint(1, 9999))
            email = fake.ascii_email()
            pw = fake.password(length=12)

            user = User.objects.create(
                username = un,
                first_name = fn,
                last_name = ln,
                email = email,
            )
            user.set_password(pw)
            user.save()

        # Customer
        for _ in range(numRecords):
            fn = fake.first_name()
            ln = fake.last_name()
            pn = fake.unique.phone_number()
            email = fake.ascii_email()
            addr = fake.street_address()
            c = fake.city()
            st = fake.administrative_unit()
            z = fake.postcode()
            s = fn + "-" + ln

            b_date = fake.date_time_this_year()
            cid = random.randint(1,numRecords)


            Customer.objects.get_or_create(
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

        # Version
        for _ in range(numRecords):
            p_image = fake.file_name(category='image')
            p_version = round(random.uniform(00.01, 99.99),2)
            p_version_date = fake.date_time_this_year()
            p_design_file = fake.file_name(extension='cad')
            p_comments = fake.paragraph()

            Version.objects.create(
                product_Image = p_image,
                product_Version = p_version,
                product_Version_Date = p_version_date,
                product_Design_File = p_design_file,
                product_Comments = p_comments,
            )
        
        # InputItems
        for _ in range(numRecords):
           input = fake.ecommerce_inputItem()
           qty = random.randint(1, 500)
           mc = fake.sentence()
           vid = random.randint(1, len(VENDORS))

           InputItem.objects.create(
               input_Name = input,
               quantity_Per_1000_Units = qty,
               vendor_id = vid,
               message_Commands = mc,
           )

        # Machine
        l = random.sample(range(1,30), 15)
        for _ in range(numRecords):
            machine_No = l[_]

            #other = random.choices(INPUT_ITEMS, k=2)
            #plastic = [INPUT_ITEMS[0]]
            #plastic.extend(other)
            print(machine_No)

            Machine.objects.create(
                machine_Number = machine_No,
                #inputID = ,
                
            )

        # Employee
        for _ in range(numRecords):
            fn = fake.first_name()
            ln = fake.last_name()
            pn = fake.unique.phone_number()
            email = fake.ascii_company_email()
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
    
        # Job
        for _ in range(numRecords):
            st = fake.past_datetime(start_date='-30d')
            et = fake.past_datetime(start_date='-10d')
            qc = fake.paragraph()
            dc = random.randint(50,400)

            mach_id = random.randint(1, numRecords)
            eid = random.randint(1, numRecords)

            Job.objects.create(
                machine_ID_id = mach_id, 
                employee_id = eid,
                start_Time = st,
                end_Time = et,
                quality_Comments = qc,
                defect_Count = dc,
                
            )
        
        # Products
        for _ in range(numRecords):
            cid = random.randint(1, len(CATEGORIES))
            mid = random.randint(1, len(MATERIAL_TYPES))
            vid = random.randint(1, numRecords)
            jid = random.randint(1, numRecords)


            Product.objects.create(
                product_Name = fake.ecommerce_product(),
                product_Description = fake.paragraph(),
                product_Price = round(random.uniform(0.01, 100),2),
                height = round(random.uniform(0.1, 100),1),
                width = round(random.uniform(0.1, 100),1),
                depth = round(random.uniform(0.1, 100),1),

                category_ID_id = cid,
                material_ID_id = mid,
                version_ID_id = vid,
                job_ID_id = jid,
            )
            
        # Cart
        cust_id = random.randint(2, numRecords + 1)
        Cart.objects.create(customer_id = cust_id)

        # CartItem
        for _ in range(1,3):
            i_qty = random.randint(1,500)
            pid = random.randint(2, numRecords + 1)
            cid = 1

            CartItem.objects.create(
                cart_id = cid,
                product_id_id = pid,
                item_quantity = i_qty,
            )
        
        # Billing
        for _ in range(numRecords):
            addr = fake.street_address()
            c = fake.city()
            st = fake.administrative_unit()
            z = fake.postcode()
            b_date = fake.past_datetime(start_date='-10d')

            cust_id = random.randint(1, numRecords)

            Billing.objects.create(
                customer_id = cust_id,
                billing_Address = addr,
                billing_City = c,
                billing_State = st,
                billing_Zip = z,
                date_Billed = b_date,
            )
        
        # Shipping
        for _ in range(numRecords):
            addr = fake.street_address()
            c = fake.city()
            st = fake.administrative_unit()
            z = fake.postcode()

            s_date = fake.past_datetime(start_date='-5d')
            
            cust_id = random.randint(1, numRecords)
            eid = random.randint(1, len(EXPEDITERS))
            
            sc = round(random.uniform(4.99, 20),2)
            sqty = random.randint(1, 30)
            swt = round(random.uniform(0.01, 500),2)

            Shipping.objects.create(
                customer_id = cust_id,
                shipping_Address = addr,
                shipping_City = c,
                shipping_State = st,
                shipping_Zip = z,
                date_Shipped = s_date,
                
                expediter_ID_id = eid,

                shipment_Cost = sc,
                shipment_Quantity = sqty, 
                shipment_Weight = swt,
            )

        # Orders
        for _ in range(numRecords):
            o_date = fake.past_datetime(start_date='-40d')
            status = fake.ecommerce_status()
            c_no = fake.password(length=25, special_chars=False, upper_case=True)
            subt = round(random.uniform(5.99, 1000),2)
            t = subt + round(random.uniform(0, 100),2)

            cust_id = random.randint(2, numRecords + 1)
            bid = random.randint(2, numRecords + 1)
            sid = random.randint(2, numRecords + 1)

            Order.objects.create(
                customer_id = cust_id,
                order_Date = o_date, 
                order_Status = status,
                confirmation_Number = c_no, 
                billing_ID_id = bid,
                shipment_ID_id = sid,
                subtotal = subt,
                total = t,
            )
        '''


            #check_category = Category.objects.all().count()
            #self.stdout.write(self.style.SUCCESS(f'Number of categories: {check_category}'))