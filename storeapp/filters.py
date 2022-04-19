import django_filters
from django_filters import DateFilter

from .models import *

class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="order_Date", lookup_expr='gte')
    end_date = DateFilter(field_name="order_Date", lookup_expr='lte')
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'order_Date', 'billing_ID', 'shipment_ID', 'subtotal', 'total', 'date_created']