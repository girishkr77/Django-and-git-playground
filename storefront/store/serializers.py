from decimal import Decimal
from rest_framework import serializers

from store.models import Product,Collection,Review

class collectionserilalizer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id','title','product_count']

    product_count = serializers.IntegerField(read_only=True)

class productSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title','slug','inventory','price','collection']
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # unit_price = serializers.DecimalField(max_digits=6,decimal_places=2, source = 'price')
    # tax_price = serializers.SerializerMethodField(method_name='tax_calculated')
    # to get a id
    collection = serializers.PrimaryKeyRelatedField(
        queryset = Collection.objects.all()
    )
    # to get a string
    # collection = serializers.StringRelatedField()
    # to get a nested json in json
    # collection = collectionserilalizer()
    # to get a hyper link
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset = Collection.objects.all(),
    #     view_name = 'collection-details' 
    # )


    def tax_calculated(self,product:Product):
        return product.price*Decimal(1.1)
    
class reviewserlizer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','name','description','date']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)