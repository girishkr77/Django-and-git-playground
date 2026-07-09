from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from.models import Product,Collection,OrderItem
from .serializers import productSerializers,collectionserilalizer
from rest_framework import status
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet 
from rest_framework.views import APIView
from django.db.models.aggregates import Count,Max,Min,Avg,Sum

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = productSerializers

    def get_serializer_context(self):
        return {'request':self.request}
    
    def destroy(self, request, *args, **kwargs):
         if OrderItem.objects.filter(product_id = kwargs['pk']).count() > 0:
            return Response({"error" : "product can't deleted as orders are associated with it."}
                            ,status=status.HTTP_405_METHOD_NOT_ALLOWED)
         return super().destroy(request, *args, **kwargs)
    
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(product_count = Count('products')).all()
    serializer_class = collectionserilalizer

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id = kwargs['pk']).count() > 0:
            return Response({"error":"cant delete collection as products associated with it"})
        return super().destroy(request, *args, **kwargs)


    
