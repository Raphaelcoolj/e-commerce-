import django_filters
from rest_framework import filters
from api.models import Product 

class Productfilter(django_filters.FilterSet):
    class Meta:
       model = Product
       fields= {
           'name':['iexact', 'icontain'],
           'price':['exact', 'lt', 'gt', 'range']
           }