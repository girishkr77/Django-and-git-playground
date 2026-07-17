from rest_framework.response import Response
from .permissions import IsadminOrReadOnly,Fulldjangomodelpermissions,Viewhistoryofcustomer
from.models import Product,Collection,OrderItem,Review,Cart,CartItem,Customer,Order
from .serializers import productSerializers,collectionserilalizer,reviewserlizer,cartserilizer,Cartitemsserlizer,getcaritemsermizer,updatecartitemserlizer,customerserializer,orderserilizer,createorderserlizer,updateorderserilizer
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser,DjangoModelPermissions,DjangoModelPermissionsOrAnonReadOnly
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,UpdateModelMixin
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
    permission_classes = [IsadminOrReadOnly]
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
    permission_classes = [IsadminOrReadOnly]

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


class Customerviewset(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = customerserializer
    permission_classes = [IsAdminUser]


    @action(detail=True,permission_classes = [Viewhistoryofcustomer])
    def history(self,request,pk):
        return Response('ok')

    @action(detail=False,methods=['get','put'],permission_classes = [IsAuthenticated])
    def me(self,request):
        (customer,created) = Customer.objects.get_or_create(user_id=request.user.id)
        if request.method == 'GET':
            serilizer = customerserializer(customer)
            return Response(serilizer.data )
        elif request.method == 'PUT':
            serilizer = customerserializer(customer)
            serilizer.is_valid()
            serilizer.save()
            return (serilizer.data)
        
class OrderViewset(ModelViewSet):

    http_method_names = ['get','post','patch','delete','head','options']

    def get_permissions(self):
        if self.request.method in ['PATCH','DELETE']:
            return [IsAdminUser()]
        return[IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serlizer = createorderserlizer(data = request.data, context = {'user_id':self.request.user.id})
        serlizer.is_valid(raise_exception=True)
        order = serlizer.save()
        serlizer = orderserilizer(order)
        return Response(serlizer.data)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return createorderserlizer
        elif self.request.method == 'PATCH':
            return updateorderserilizer
        return orderserilizer
    
    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.all()
        
        (customer_id,created) = Customer.objects.only('id').get_or_create(user_id = user.id)
        return Order.objects.filter(customer_id = customer_id)

