from multiprocessing import AuthenticationError
import random
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
import json

from django.forms import inlineformset_factory

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from faker import Faker

# Create your views here.
from .models import *
from .forms import OrderForm, ProductForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from .decorators import allowed_users, unauthenticated_user, admin_only


def homePage(request):
    if request.user.is_authenticated and not request.user.is_staff:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

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

    context = {'form': form}
    return render(request, 'storeapp/register.html', context)


@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('customer_dashboard')
        else:
            messages.info(request, 'Username AND/OR Password is incorrect')

    context = {}
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
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'storeapp/product_listing.html', context)

def shoppingCart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0 }
        cartItems = order['get_cart_items']

    context = {'items':items, 'order': order, 'cartItems': cartItems}
    return render(request, 'storeapp/shopping_cart.html', context )

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0 }
        cartItems = order['get_cart_items']

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

        order, created = Order.objects.get_or_create(
            customer = customer, 
            complete = True,
            confirmation_Number = transaction_id,
            order_Status = 'Pending',
            )

        order.save()
        
        Shipping.objects.create(
            customer=customer,
            order=order,

            shipping_Address=data['shipping']['address'],
            shipping_City=data['shipping']['city'],
            shipping_State=data['shipping']['state'],
            shipping_Zip=data['shipping']['zipcode'],
            
            shipment_Cost = round(random.uniform(4.99, 20),2),
            shipment_Quantity = order.get_cart_total,
            shipment_Weight = round(random.uniform(0.01, 500),2),
        )
        
    else:
        print('User is not logged in')

    return JsonResponse('Payment Completed', safe=False)


def productDetails(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'storeapp/productDetails.html', {'product': product})

def productsPage(request):
    products = Product.objects.all()
    return render(request, 'storeapp/products.html', {'products': products})






@login_required(login_url='login')
@admin_only
def employee_dashboard(request):
    orders = Order.objects.all()
    products = Product.objects.all()

    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders = orders.filter(complete=True).count()
    delivered = orders.filter(order_Status='Delivered').count()
    pending = orders.filter(order_Status='Pending').count()

    context = {'orders':orders, 'products':products, 'customers':customers,
    'total_orders':total_orders,'delivered':delivered,
    'pending':pending}

    return render(request, 'storeapp/employee_dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def customer_dashboard(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
        
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    delivered = orders.filter(order_Status='Delivered').count()
    pending = orders.filter(order_Status='Pending').count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    

    context = {'orders':orders, 'total_orders':total_orders,'delivered':delivered,
    'pending':pending, 'myFilter': myFilter, 'cartItems': cartItems }

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
def updateCustomer(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)    

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_dashboard')

    context = {'form': form}
    return render(request, 'storeapp/account_settings.html', context)


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
            return redirect('/')
    
    context = {'formset': formset}
    return render(request, 'storeapp/orderUpdateForm.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'employee'])
def updateOrder(request, pk):

    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)    

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'storeapp/update.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'employee'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    context = {'item': order}
    return render(request, 'storeapp/delete.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'employee'])
def createProduct(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
    
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
            return redirect('/')

    context = {'form': form}
    return render(request, 'storeapp/update.html', context)
