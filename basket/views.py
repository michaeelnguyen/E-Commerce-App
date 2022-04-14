from django.shortcuts import render

# Create your views here.

def basket_summary(request):
    return render(request, 'storeapp/basket/summary.html')