from django.shortcuts import render
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from .models import *

# Create your views here.

def homePage(request):
    return render(request, 'storeapp/home.html')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'storeapp/register.html', context)

def loginPage(request):
    context = {}
    return render(request, 'storeapp/login.html', context )

def productListing(request):
    products = Product.objects.all()
    return render(request, 'storeapp/product_listing.html', {'products': products})

def productDetails(request):
    context = {}
    return render(request, 'storeapp/productDetails.html', context)

def productsPage(request):
    products = Product.objects.all()
    return render(request, 'storeapp/products.html', {'products': products})

def shoppingCart(request):
    context = {}
    return render(request, 'storeapp/shopping_cart.html', context )

def employee_dashboard(request, pk):
    employee = Employee.objects.get(id=pk)
    orders = Order.objects.all()
    products = Product.objects.all()

    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(order_Status='Delivered').count()
    pending = orders.filter(order_Status='Pending').count()

    context = {'employee':employee,'orders':orders, 'products':products, 'customers':customers,
    'total_orders':total_orders,'delivered':delivered,
    'pending':pending}

    return render(request, 'storeapp/employee_dashboard.html', context)

def customer_dashboard(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    
    total_orders = orders.count()
    delivered = orders.filter(order_Status='Delivered').count()
    pending = orders.filter(order_Status='Pending').count()

    context = {'orders':orders, 'customer':customer,
    'total_orders':total_orders,'delivered':delivered,
    'pending':pending }

    return render(request, 'storeapp/customer_dashboard.html', context)