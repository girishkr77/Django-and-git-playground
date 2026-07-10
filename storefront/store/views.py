from rest_framework.response import Response
from.models import Product,Collection,OrderItem,Review
from .serializers import productSerializers,collectionserilalizer,reviewserlizer
from rest_framework import status
from rest_framework.viewsets import ModelViewSet 
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models.aggregates import Count
from .filters import productfilters
from .paginatiom import DefaultPagination


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = productSerializers
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    # filterset_fields = ['collection_id']
    pagination_class = DefaultPagination
    filterset_class = productfilters
    search_fields = ['title','description']
    ordering_fields = ['price']
    


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


class ReviewViewSet(ModelViewSet):
    serializer_class = reviewserlizer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}

