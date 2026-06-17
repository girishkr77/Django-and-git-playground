from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist 
from store.models import Product,Customer,Order,OrderItem,Collection
from tags.models import TaggedItem,taggedItemManager
from django.db.models import Q,F,Value,Func,DecimalField
from django.db.models.aggregates import Count,Max,Min,Avg,Sum
from django.db.models.functions import Concat
from django.db.models import ExpressionWrapper
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

# Create your views here.

def helloword(request):
    # query_set = Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')
    # query_set = Product.objects.only('id','title')
    # query_set = Product.objects.prefetch_related('promotioms').select_related('collection').all()
    # query_set = OrderItem.objects.select_related('product').all(id__in = latest_order)
    # result = Product.objects.aggregate(count = Count('id'), min_pricce = Max('price')) 
    # result = Product.objects.filter(collection_id__in=Collection.objects.filter(title__exact='jai balaya'))
    # fixed_output = ExpressionWrapper(F('price') * 0.8, output_field = DecimalField())
    # result = Product.objects.annotate(
        # full_name = Func(F('first_name'),Value(' '),F('Last_name'),function='CONCAT')
        # full_name = Concat(('first_name'),Value(' '),('Last_name'))
        # orders_count = Count('order')
        # discount_price = fixed_output
    # ) 
    # content_type = ContentType.objects.get_for_model(Product)

    # query_set = TaggedItem.objects\
    #     .select_related('tag')\
    #         .filter(content_type=content_type,object_id=1)

    # query_set = TaggedItem.objects.get_taged_item( Product, 1)

    # collection = Collection()
    # collection.title = 'jai balaya akanda'
    # collection.feature_product = Product(pk=1)
    # collection.save()

    # Collection.objects.filter(pk=101).delete()
    # with transaction.atomic():      
    #     order = Order()
    #     order.customer_id = 1
    #     order.save()

    #     item = OrderItem()
    #     item.order = order
    #     item.product_id = -1
    #     item.quantity = 3
    #     item.item_prize = 35
    #     item.save()


    #-------assignment---------------------------------------
    # query_set = Order.objects.filter(payment_status__iexact='F')

    # query_set = Product.objects.filter(price__range=(10,30))

    # query_set = Order.objects.order_by('-placed_at')[:10]

    # query_set = Order.objects.filter(payment_status__iexact = 'P').count

    # query_set = Product.objects.filter(collection_id__in=Collection.objects.filter(title__iexact='jai balaya'))

    # query_set = Order.objects.filter(payment_status__iexact='C').values('customer__first_name').distinct()

    # query_set = OrderItem.objects.filter(product__in=Product.objects.filter(id__in=Collection.objects.filter(title__iexact='jai balaya')))

    # query_set = Order.objects.filter(customer__in=Customer.objects.filter(first_name__iexact = 'Min'))

    # query_set = Product.objects.aggregate(highest_price = Max('price'))

    # query_set = OrderItem.objects.aggregate(physical_count = Sum('quantity'))

    # query_set = OrderItem.objects.filter(order__exact=2).aggregate(total_revenue = Sum('item_prize'))

    query_set = Collection.objects.values('title').annotate(product_count = Count('product'))


    return render(request,'hello.html',{'name':'jaibalaya','orders':query_set})
