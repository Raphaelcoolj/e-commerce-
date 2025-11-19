import django_filters
from rest_framework import filters
from .models import Product 

class ProductFilter(django_filters.FilterSet):
    class Meta:
       model = Product
       fields= {
           'name':['iexact', 'icontains'],
           'price':['exact', 'lt', 'gt', 'range']
           }