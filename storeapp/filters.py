from django.forms import ModelChoiceField
import django_filters
from django_filters import DateFilter, ChoiceFilter, ModelChoiceFilter, CharFilter

from .models import *
from .forms import *

STATUS = (
    ('Pending', 'Pending'),
    ('Shipped', 'Shipped'),
    ('Out for Delivery', 'Out for Delivery'),
    ('Delivered', 'Delivered'),
    ('Canceled', 'Canceled'),
)


class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="order_Date", lookup_expr='gte')
    end_date = DateFilter(field_name="order_Date", lookup_expr='lte')
    
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['complete', 'customer', 'total', 'date_created', 'is_active']

class OrderItemFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="order__order_Date", lookup_expr='gte', label='Order Start Date', widget=DateTimeInput)
    end_date = DateFilter(field_name="order__order_Date", lookup_expr='lte', label='Order End Date', widget=DateTimeInput)
    order__order_Status = ChoiceFilter(choices=STATUS, label='Order Status')
    order__confirmation_Number = CharFilter(field_name="order__confirmation_Number", lookup_expr='icontains', label="Confirmation #")

    class Meta:
        model = OrderItem
        fields = ['order__order_Status', 'order__confirmation_Number']
        
