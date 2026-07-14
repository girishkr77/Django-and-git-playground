from rest_framework.response import Response
from.models import Product,Collection,OrderItem,Review,Cart,CartItem
from .serializers import productSerializers,collectionserilalizer,reviewserlizer,cartserilizer,Cartitemsserlizer,getcaritemsermizer,updatecartitemserlizer
from rest_framework import status
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView
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


class Cartsetview(ModelViewSet):
    queryset = Cart.objects.prefetch_related('carts__product').all()
    serializer_class = cartserilizer

class CartitemViewset(ModelViewSet):
    http_method_names = ['get','post','patch','delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return getcaritemsermizer
        if self.request.method == 'PATCH':
            return updatecartitemserlizer
        return Cartitemsserlizer
    
    def get_serializer_context(self):
        return {'cart_id':self.kwargs['cart_pk']}
    

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk'])