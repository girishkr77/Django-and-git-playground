from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from.models import Product,Collection
from .serializers import productSerializers,collectionserilalizer,collectionserilalizerforcreate
from rest_framework import status
from django.db.models.aggregates import Count,Max,Min,Avg,Sum

@api_view(['GET','POST'])
def product_list (request):
    if request.method == 'GET':
        products = Product.objects.select_related('collection').all().order_by('id')
        serlizer = productSerializers(products, many = True, context = {'request':request})
        return Response(serlizer.data)
    elif request.method == 'POST':
        serlizer = productSerializers(data=request.data)
        # if 
        serlizer.is_valid(raise_exception=True)
        serlizer.save()
        # print(serlizer.validated_data)
        return Response(serlizer.data, status=status.HTTP_201_CREATED)
        # else: 
        #      return Response(serlizer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def product_detailes(request, id):
        product = get_object_or_404(Product,pk=id)
    # try:
        # product = Product.objects.get(pk=id)
        if request.method == 'GET':
            
            serlizer = productSerializers(product)
            return Response(serlizer.data)
        elif request.method == 'PUT':
            serlizer = productSerializers(product,data = request.data)
            serlizer.is_valid()
            serlizer.save()
            return Response(serlizer.data)
        elif request.method == 'DELETE':
            if product.orderitems.count() > 0:
                 return Response({"error" : "product can't deleted as orders are associated with it."},status=status.HTTP_405_METHOD_NOT_ALLOWED)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    # except Product.DoesNotExist:
        # return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET','POST'])
def collection_list(request):
    if request.method == 'GET':
        collection = Collection.objects.annotate(product_count = Count('products')).all()
        serlizer = collectionserilalizer(collection, many = True)
        return Response(serlizer.data)
    elif request.method == 'POST':
        serlizer = collectionserilalizerforcreate(data = request.data)
        serlizer.is_valid(raise_exception=True)
        serlizer.save()
        return Response(serlizer.data)
    
@api_view(['GET','PUT','DELETE'])
def collection_detailes(request,pk):
    collections = Collection.objects.get(pk=pk)
    if request.method == 'GET':
        collection = get_object_or_404(Collection.objects.annotate(product_count = Count('products')),pk = pk)
        serlizer = collectionserilalizer(collection)
        return Response(serlizer.data)
    elif request.method == 'PUT':
        serlizer = collectionserilalizerforcreate(collections,data=request.data)
        serlizer.is_valid(raise_exception=True)
        serlizer.save()
        return Response(serlizer.data,status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        if collections.products.count() > 0:
            return Response({"error":"cant delete collection as products associated with it"})
        collections.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
