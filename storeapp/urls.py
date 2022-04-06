from django.urls import path
from . import views
from storeapp import views as storeapp_views

urlpatterns = [
    path('', storeapp_views.productListing, name="productListing"),
    path('register/', storeapp_views.registerPage, name="register"),
    path('login/', storeapp_views.loginPage, name="login"),
]