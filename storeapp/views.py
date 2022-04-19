from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from .models import *
from .forms import OrderForm, ProductForm
from .filters import OrderFilter

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

def productDetails(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'storeapp/productDetails.html', {'product': product})

def productsPage(request):
    products = Product.objects.all()
    return render(request, 'storeapp/products.html', {'products': products})

def shoppingCart(request):
    context = {}
    return render(request, 'storeapp/shopping_cart.html', context )

def employee_dashboard(request):
    orders = Order.objects.all()
    products = Product.objects.all()

    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(order_Status='Delivered').count()
    pending = orders.filter(order_Status='Pending').count()

    context = {'orders':orders, 'products':products, 'customers':customers,
    'total_orders':total_orders,'delivered':delivered,
    'pending':pending}

    return render(request, 'storeapp/employee_dashboard.html', context)

def customer_dashboard(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    
    total_orders = orders.count()
    delivered = orders.filter(order_Status='Delivered').count()
    pending = orders.filter(order_Status='Pending').count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'orders':orders, 'customer':customer,
    'total_orders':total_orders,'delivered':delivered,
    'pending':pending, 'myFilter': myFilter }

    return render(request, 'storeapp/customer_dashboard.html', context)


''' def createCustomer(request):
    form = CustomerRegistrationForm()
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
    
    context = {'form': form}
    return render(request, 'storeapp/update.html', context)

def updateCustomer(request, pk):
    
    customer = Customer.objects.get(id=pk)
    form = CustomerRegistrationForm(instance=customer)    

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'storeapp/update.html', context) '''



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

def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    context = {'item': order}
    return render(request, 'storeapp/delete.html', context)



def createProduct(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
    
    context = {'form': form}
    return render(request, 'storeapp/update.html', context)

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