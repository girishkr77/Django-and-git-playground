from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from.models import Product
from .serializers import productSerializers
from rest_framework import status

@api_view()
def product_list (request):
    products = Product.objects.all().order_by('id')
    serlizer = productSerializers(products, many = True)
    return Response(serlizer.data)

@api_view()
def product_detailes(request, id):
    # try:
        # product = Product.objects.get(pk=id)
        product = get_object_or_404(Product,pk=id)
        serlizer = productSerializers(product)
        return Response(serlizer.data)
    # except Product.DoesNotExist:
        # return Response(status=status.HTTP_404_NOT_FOUND)