from unicodedata import name
from django.urls import path
from . import views
from storeapp import views as storeapp_views

urlpatterns = [
    path('', storeapp_views.homePage, name="home"),
    path('register/', storeapp_views.registerPage, name="register"),
    path('login/', storeapp_views.loginPage, name="login"),
    path('products/', storeapp_views.productsPage, name="products"),
    path('shop/', storeapp_views.productListing, name="productListing"),
    
    path('shop/productDetails/<str:pk>/', storeapp_views.productDetails, name="productDetails"),
    #path('productDetails/<str:pk>/', storeapp_views.productDetails, name="productDetails"),

    path('admin_dashboard/', storeapp_views.employee_dashboard, name="employee_dashboard"),
    path('dashboard/<str:pk>/', storeapp_views.customer_dashboard, name="customer_dashboard"),
    path('admin_dashboard/', storeapp_views.employee_dashboard, name="employee_dashboard"),
    #path('dashboard/', storeapp_views.customer_dashboard, name="customer_dashboard"),
    path('shoppingCart/', storeapp_views.shoppingCart, name="shoppingCart"),

    path('create_order/<str:pk>/', storeapp_views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', storeapp_views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', storeapp_views.deleteOrder, name="delete_order"),

#    path('create_customer/', storeapp_views.createCustomer, name="create_customer"),
#    path('update_customer/<str:pk>/', storeapp_views.updateCustomer, name="update_customer"),

    path('create_product/', storeapp_views.createProduct, name="create_product"),
    path('update_product/<str:pk>/', storeapp_views.updateProduct, name="update_product"),

]