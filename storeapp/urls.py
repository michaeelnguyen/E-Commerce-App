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


    path('products/<str:pk>/', storeapp_views.productsPage, name="products"),

    
    path('shop/', storeapp_views.productListing, name="productListing"),
    path('cart/', storeapp_views.shoppingCart, name="shoppingCart"),
    path('checkout/', storeapp_views.checkout, name="checkout"),
    
    path('update_item/', storeapp_views.updateItem, name="update_item"),
    path('process_order/', storeapp_views.processOrder, name="process_order"),

    path('shop/productDetails/<str:pk>/', storeapp_views.productDetails, name="productDetails"),


    path('admin_dashboard/', storeapp_views.employee_dashboard, name="employee_dashboard"),
    
    path('dashboard/', storeapp_views.customer_dashboard, name="customer_dashboard"),
    path('dashboard/<str:pk>/', storeapp_views.customer_dashboard, name="customer_dashboard2"),

    path('create_order/<str:pk>/', storeapp_views.createOrder, name="create_order"),
    path('view_order/<str:pk>', storeapp_views.viewOrder, name='view_order'),
    path('update_order/<str:pk>/', storeapp_views.updateOrder, name="update_order"),
    path('cancel_order/<str:pk>/', storeapp_views.cancelOrder, name="cancel_order"),

    #path('create_customer/', storeapp_views.createCustomer, name="create_customer"),
    path('update_customer/', storeapp_views.accountSettings, name="update_customer"),
    path('update_customer/<str:pk>/', storeapp_views.updateCustomer, name="update_customer2"),

    path('create_product/', storeapp_views.createProduct, name="create_product"),
    path('update_product/<str:pk>/', storeapp_views.updateProduct, name="update_product"),


    path('create_job/', storeapp_views.createJob, name="create_job"),
    path('update_job/<str:pk>/', storeapp_views.updateJob, name="update_job"),

    path('create_version/', storeapp_views.createVersion, name="create_version"),
    path('update_version/<str:pk>/', storeapp_views.updateVersion, name="update_version"),

    path('create_machine/', storeapp_views.createMachine, name="create_machine"),
    path('update_machine/<str:pk>/', storeapp_views.updateMachine, name="update_machine"),

    path('create_input/', storeapp_views.createInput, name="create_input"),
    path('update_input/<str:pk>/', storeapp_views.updateInput, name="update_input"),

    path('create_custom_admin/', storeapp_views.createCustomAdmin, name="create_custom_admin"),
    
    path('create_custom_version/<str:pk>/', storeapp_views.createCustomVersion, name="create_custom_version"),
    path('update_custom_version/<str:pk>/', storeapp_views.updateCustomVersion, name="update_custom_version"),

    path('create_custom_product/<str:pk>/', storeapp_views.createCustomProduct, name="create_custom_product"),
    path('update_custom_product/<str:pk>/', storeapp_views.updateCustomProduct, name="update_custom_product"),

    path('update_orderitem/<str:pk>', storeapp_views.updateOrderItem, name='update_orderitem'),



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