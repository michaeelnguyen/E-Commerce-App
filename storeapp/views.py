import random
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
import json

from django.forms import inlineformset_factory

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.urls import reverse
from multi_form_view import MultiModelFormView
from faker import Faker

# Create your views here.
from .models import *
from .forms import BillingForm, CustomProductForm, CustomVersionForm, EditOrderForm, InputForm, JobForm, MachineForm, OrderForm, OrderItemForm, ProductForm, CreateUserForm, CustomerForm, ShippingForm, VersionForm, ViewOrderForm, ViewOrderItemForm
from .filters import OrderFilter, OrderItemFilter
from .decorators import allowed_users, unauthenticated_user, admin_only
from .utils import cookieCart, cartData, guestOrder


def homePage(request):
    if request.user.is_authenticated and not request.user.is_staff:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']

    context = {'cartItems': cartItems}
    return render(request, 'storeapp/home.html', context)


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' +  username)

            return redirect('login')
    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'form': form,'items':items, 'order': order, 'cartItems': cartItems}
    return render(request, 'storeapp/register.html', context)


@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('productListing')
        else:
            messages.info(request, 'Username AND/OR Password is incorrect')

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    context = {'items':items, 'order': order, 'cartItems': cartItems}
    return render(request, 'storeapp/login.html', context )

@unauthenticated_user
def emp_loginPage(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('employee_dashboard')
        else:
            messages.info(request, 'Username AND/OR Password is incorrect')

    context = {}
    return render(request, 'storeapp/employee_login.html', context )


def logoutUser(request):
    logout(request)
    return redirect('login')



def productListing(request):

    if request.user.is_authenticated and not request.user.is_staff:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        #items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        products = Product.objects.all()
        context = {'products': products, 'cartItems': cartItems, 'customer': customer}
        return render(request, 'storeapp/product_listing.html', context)
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'storeapp/product_listing.html', context)

def shoppingCart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order': order, 'cartItems': cartItems}
    return render(request, 'storeapp/shopping_cart.html', context )

def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order': order, 'cartItems': cartItems}
    return render(request, 'storeapp/checkout.html', context )


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    fake = Faker()
    transaction_id = fake.bothify(text='??##??##??##')
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer

        order, created = Order.objects.get_or_create(customer = customer, complete = False)

        order.order_Status = 'Pending'
        order.confirmation_Number = transaction_id
        order.total = order.get_cart_total
        order.complete = True
        order.save()
        
        Shipping.objects.create(
            customer=customer,
            order=order,

            shipping_Address=data['shipping']['address'],
            shipping_City=data['shipping']['city'],
            shipping_State=data['shipping']['state'],
            shipping_Zip=data['shipping']['zipcode'],
            
            shipment_Cost = round(random.uniform(4.99, 20),2),
            shipment_Quantity = order.get_cart_items,
            shipment_Weight = round(random.uniform(0.01, 500),2),
        )

        Billing.objects.create(
            customer=customer,
            order=order,

            billing_Address=data['billing']['address'],
            billing_City=data['billing']['city'],
            billing_State=data['billing']['state'],
            billing_Zip=data['billing']['zipcode'],
        )
        
    else:
        customer, order = guestOrder(request, data)
        order.complete = True
        order.save()

    return JsonResponse('Payment Completed', safe=False)


def productDetails(request, pk):
    product = Product.objects.get(id=pk)

    if request.user.is_authenticated and not request.user.is_staff:
        data = cartData(request)
        cartItems = data['cartItems']
        order = data['order']
        items = data['items']
        context = {'product': product, 'items':items, 'order': order, 'cartItems': cartItems}
    


    context = {'product': product}
    return render(request, 'storeapp/productDetails.html', context)



def productsPage(request,pk):
    customer = Customer.objects.get(id=pk)

    versions = Version.objects.filter(customer=customer)
    products = Product.objects.all()
    
    return render(request, 'storeapp/products.html', {'customer': customer, 'products': products, 'versions': versions})






@login_required(login_url='login')
@admin_only
def employee_dashboard(request):
    orders = Order.objects.all()
    products = Product.objects.all()
    customers = Customer.objects.all()
    jobs = Job.objects.all()
    versions = Version.objects.all()
    machines = Machine.objects.all()
    inputs = InputItem.objects.all()
    order_items = OrderItem.objects.all()

    total_customers = customers.count()
    total_orders = orders.filter(complete=True).count()
    delivered = orders.filter(order_Status='Delivered').count()
    pending = orders.filter(order_Status='Pending').count()

    context = {'orders':orders, 'products':products, 'customers':customers, 'jobs':jobs, 'versions':versions, 'machines':machines, 'inputs': inputs,
    'total_orders':total_orders,'delivered':delivered,
    'pending':pending, 'order_items':order_items}

    return render(request, 'storeapp/employee_dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def customer_dashboard(request, pk):

    if request.user.is_authenticated:
        customer = request.user.customer
        #customer = Customer.objects.get(id=pk)
        order = Order.objects.get(customer=customer, complete=False)

        #order, created = Order.objects.get_or_create(customer=customer, complete=True)
        #order, created = Order.objects.filter(customer=customer, complete=True)
        if order != Order.DoesNotExist:
            items = order.orderitem_set.all()
            data = cartData(request)
            cartItems = data['cartItems']
            order = data['order']
        else:
            order, created = Order.objects.get_or_create(customer=customer, complete=True)

        
    orders = customer.order_set.all()
    order_items = OrderItem.objects.all()

    # OFF BY ONE ERROR
    total_orders = orders.filter(complete=True).count()
    
    delivered = orders.filter(order_Status='Delivered').count()
    pending = orders.filter(order_Status='Pending').count()

    myFilter = OrderItemFilter(request.GET, queryset=order_items)
    order_items = myFilter.qs
    

    context = {'orders': orders, 'total_orders': total_orders,'delivered': delivered,
    'pending':pending, 'myFilter': myFilter, 'cartItems': cartItems, 'customer': customer, 'items': items, 'order_items': order_items}

    return render(request, 'storeapp/customer_dashboard.html', context)


''' def createCustomer(request):
    form = CustomerRegistrationForm()
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
    
    context = {'form': form}
    return render(request, 'storeapp/update.html', context)
'''
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)    

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_dashboard2', pk=request.user.customer.pk)

    context = {'form': form}
    return render(request, 'storeapp/account_settings.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'employee'])
def updateCustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer)    

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('employee_dashboard')

    context = {'form': form}
    return render(request, 'storeapp/update.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'employee'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'order_Status'), extra=5)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    #form = OrderForm(initial={'customer': customer})
    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('employee_dashboard')
    
    context = {'formset': formset}
    return render(request, 'storeapp/orderUpdateForm.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'employee', 'customer'])
def updateOrder(request, pk):

    order = Order.objects.get(id=pk)
    form = EditOrderForm(instance=order)    

    if request.method == 'POST':
        form = EditOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            if request.user.is_staff:
                return redirect('employee_dashboard')
            else:
                return redirect('customer_dashboard')

    context = {'form': form}
    return render(request, 'storeapp/update.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'employee', 'customer'])
def cancelOrder(request, pk):
    if request.user.is_staff:
        user = request.user.employee
        user = Employee.objects.get(id=user.id)
    else:
        user = request.user.customer
        user = Customer.objects.get(id=user.id)

    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.order_Status = 'Cancelled'
        order.is_active = False
        order.save(update_fields=['order_Status', 'is_active'], force_update=True)

        order_items = OrderItem.objects.filter(order=order)
        for item in order_items:
            item.order=order
            item.save(update_fields=['order'], force_update=True)

        redirect('customer_dashboard2', user.id)

    context = {'order': order, 'user': user}

    return render(request, 'storeapp/cancel.html', context)






@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'employee'])
def createProduct(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_dashboard')
    
    context = {'form': form}
    return render(request, 'storeapp/update.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'employee'])
def updateProduct(request, pk):
    
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)    

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('employee_dashboard')

    context = {'form': form}
    return render(request, 'storeapp/update.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'employee'])
def createJob(request):
    form = JobForm()
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_dashboard')
    
    context = {'form': form}
    return render(request, 'storeapp/update.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'employee'])
def updateJob(request, pk):
    
    job = Job.objects.get(id=pk)
    form = JobForm(instance=job)    

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('employee_dashboard')

    context = {'form': form}
    return render(request, 'storeapp/update.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'employee'])
def createVersion(request):
    form = VersionForm()
    if request.method == 'POST':
        form = VersionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_dashboard')
    
    context = {'form': form}
    return render(request, 'storeapp/update.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'employee'])
def updateVersion(request, pk):
    
    ver = Version.objects.get(id=pk)
    form = VersionForm(instance=ver)    

    if request.method == 'POST':
        form = VersionForm(request.POST, instance=ver)
        if form.is_valid():
            form.save()
            return redirect('employee_dashboard')

    context = {'form': form}
    return render(request, 'storeapp/update.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'employee'])
def createMachine(request):
    form = MachineForm()
    if request.method == 'POST':
        form = MachineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_dashboard')
    
    context = {'form': form}
    return render(request, 'storeapp/update.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'employee'])
def updateMachine(request, pk):
    
    mach = Machine.objects.get(id=pk)
    form = MachineForm(instance=mach)    

    if request.method == 'POST':
        form = MachineForm(request.POST, instance=mach)
        if form.is_valid():
            form.save()
            return redirect('employee_dashboard')

    context = {'form': form}
    return render(request, 'storeapp/update.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'employee'])
def createInput(request):
    form = InputForm()
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_dashboard')
    
    context = {'form': form}
    return render(request, 'storeapp/update.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'employee'])
def updateInput(request, pk):
    
    input = InputItem.objects.get(id=pk)
    form = InputForm(instance=input)    

    if request.method == 'POST':
        form = InputForm(request.POST, instance=input)
        if form.is_valid():
            form.save()
            return redirect('employee_dashboard')

    context = {'form': form}
    return render(request, 'storeapp/update.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def createCustomVersion(request,pk):
    form = CustomVersionForm()
    form.fields['customer'].empty_label = None
    form.fields['customer'].queryset = Customer.objects.filter(id=pk)

    if request.method == 'POST':
        form = CustomVersionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('create_custom_product', pk=request.user.customer.pk)

    context = {'form': form}
    return render(request, 'storeapp/custom_design.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def updateCustomVersion(request, pk):
    ver = Version.objects.get(id=pk)
    form = CustomVersionForm(instance=ver)    

    if request.method == 'POST':
        form = CustomVersionForm(request.POST, instance=ver)
        if form.is_valid():
            form.save()
            return redirect('products', pk=request.user.customer.pk)

    context = {'form': form}
    return render(request, 'storeapp/update.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'employee'])
def createCustomAdmin(request):
    form = CustomVersionForm()
    if request.method == 'POST':
        form = CustomVersionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('create_custom_product')

    context = {'form': form}
    return render(request, 'storeapp/custom_design.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'employee', 'customer'])
def createCustomProduct(request, pk):
    form = CustomProductForm()
    form.fields['version_ID'].queryset = Version.objects.filter(customer=pk)
    if request.method == 'POST':
        form = CustomProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products', pk=request.user.customer.pk)

    context = {'form': form}
    return render(request, 'storeapp/custom_design2.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def updateCustomProduct(request, pk):
    
    product = Product.objects.get(id=pk)
    form = CustomProductForm(instance=product)    

    if request.method == 'POST':
        form = CustomProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products', pk=request.user.customer.pk)

    context = {'form': form}
    return render(request, 'storeapp/update.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def updateOrderItem(request, pk):
    order_item = OrderItem.objects.get(id=pk)
    form = OrderItemForm(instance=order_item)    

    if request.method == 'POST':
        form = OrderItemForm(request.POST, instance=order_item)
        if form.is_valid():
            form.save()
            return redirect('employee_dashboard')

    context = {'form': form}
    return render(request, 'storeapp/update.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def viewOrder(request, pk):
    
    order = Order.objects.get(id=pk)
    #order_item = OrderItem.objects.get(order=order)
    order_items = OrderItem.objects.filter(order=order)
    billing = Billing.objects.get(order=order)
    shipping = Shipping.objects.get(order=order)


    form = ViewOrderForm(instance=order)
    #form2 = ViewOrderItemForm(instance=order_item)
    form3 = BillingForm(instance=billing)    
    form4 = ShippingForm(instance=shipping)

    #context = {'form': form, 'form2': form2, 'form3': form3, 'form4': form4, 'order_items': order_items}
    context = {'form': form, 'form3': form3, 'form4': form4, 'order_items': order_items}
    return render(request, 'storeapp/view.html', context)