from unicodedata import name
from django.urls import path

from . import views
from storeapp import views as storeapp_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', storeapp_views.homePage, name="home"),
    path('register/', storeapp_views.registerPage, name="register"),
    path('login/', storeapp_views.loginPage, name="login"),
    path('emp_login/', storeapp_views.emp_loginPage, name='emp_login'),
    path('logout/', storeapp_views.logoutUser, name="logout"),

    path('products/', storeapp_views.productsPage, name="products"),

    
    path('shop/', storeapp_views.productListing, name="productListing"),
    path('shoppingCart/', storeapp_views.shoppingCart, name="shoppingCart"),
    path('checkout/', storeapp_views.checkout, name="checkout"),
    
    path('update_item/', storeapp_views.updateItem, name="update_item"),
    path('process_order/', storeapp_views.processOrder, name="process_order"),

    path('shop/productDetails/<str:pk>/', storeapp_views.productDetails, name="productDetails"),


    path('admin_dashboard/', storeapp_views.employee_dashboard, name="employee_dashboard"),
    #path('dashboard/<str:pk>/', storeapp_views.customer_dashboard, name="customer_dashboard"),
    path('dashboard/', storeapp_views.customer_dashboard, name="customer_dashboard"),

    path('create_order/<str:pk>/', storeapp_views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', storeapp_views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', storeapp_views.deleteOrder, name="delete_order"),

    #path('create_customer/', storeapp_views.createCustomer, name="create_customer"),
    path('update_customer/', storeapp_views.updateCustomer, name="update_customer"),

    path('create_product/', storeapp_views.createProduct, name="create_product"),
    path('update_product/<str:pk>/', storeapp_views.updateProduct, name="update_product"),




    path('reset_password/',
        auth_views.PasswordResetView.as_view(template_name="storeapp/password_reset.html"),
        name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="storeapp/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name="storeapp/password_reset_form.html"), 
        name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="storeapp/password_reset_done.html"), 
        name="password_reset_complete"),

]