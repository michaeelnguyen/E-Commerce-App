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
    context = {}
    return render(request, 'storeapp/product_listing.html', context)

def productsPage(request):
    products = Product.objects.all()
    return render(request, 'storeapp/products.html', {'products': products})
