from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist 
from store.models import Product,Customer,Order,OrderItem,Collection
from tags.models import TaggedItem,taggedItemManager
from django.db.models import Q,F,Value,Func,DecimalField
from django.db.models.aggregates import Count,Max,Min,Avg
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
    with transaction.atomic():
        order = Order()
        order.customer_id = 1
        order.save()

        item = OrderItem()
        item.order = order
        item.product_id = -1
        item.quantity = 3
        item.item_prize = 35
        item.save()


    return render(request,'hello.html',{'name':'jaibalaya'})
