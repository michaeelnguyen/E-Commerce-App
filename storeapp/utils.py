import json

from faker import Faker
from .models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    print('Cart:', cart)
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0 }
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.product_Price * cart[i]['quantity'])
            
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product':{
                    'id': product.id,
                    'product_Name': product.product_Name,
                    'product_Price': product.product_Price,
                    'imageURL': product.imageURL,
                },
                'quantity': cart[i]['quantity'],
                'get_total': total,
            }
            items.append(item)
        
        except:
            pass
    return {'cartItems': cartItems, 'order': order, 'items': items}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return {'cartItems': cartItems, 'order': order, 'items': items}

def guestOrder(request, data):
    print('User is not logged in')

    fake = Faker()
    transaction_id = fake.bothify(text='??##??##??##')


    print('COOKIES:', request.COOKIES)
    name = data['form']['name'].split(' ')
    email = data['form']['email']

    cookieData = cookieCart(request)
    cartItems = cookieData['cartItems']
    order = cookieData['order']
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(
        customer_Email=email,
        #customer_Phone_Number=pn,
    )
    customer.customer_First_Name = name[0]
    customer.customer_Last_Name = name[1]
    customer.slug = name[0] + name[1]

    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=True,
        confirmation_Number = transaction_id,
        order_Status = 'Pending',
        total = order['get_cart_total'],
        
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        orderItem = OrderItem.objects.create(
            product = product,
            order=order,
            quantity=item['quantity']
        )

    return customer, order

