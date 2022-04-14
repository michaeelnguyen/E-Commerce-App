from django.urls import path
from . import views
from storeapp import views as storeapp_views

urlpatterns = [
    path('', storeapp_views.homePage, name="home"),
    path('register/', storeapp_views.registerPage, name="register"),
    path('login/', storeapp_views.loginPage, name="login"),
    path('products/', storeapp_views.productsPage, name="products"),
    path('shop/', storeapp_views.productListing, name="productListing"),
    path('admin_dashboard/<str:pk>/', storeapp_views.employee_dashboard, name="employee_dashboard"),
    path('dashboard/<str:pk>/', storeapp_views.customer_dashboard, name="customer_dashboard"),
    #path('admin_dashboard/', storeapp_views.employee_dashboard, name="employee_dashboard"),
    #path('dashboard/', storeapp_views.customer_dashboard, name="customer_dashboard"),

]