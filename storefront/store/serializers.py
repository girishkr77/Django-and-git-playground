from decimal import Decimal
from rest_framework import serializers

from store.models import Product,Collection,Review,Cart,CartItem

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


    # def tax_calculated(self,product:Product):
    #     return product.price*Decimal(1.1)
    
class reviewserlizer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','name','description','date']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)
    
class simpleproductserlizer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title','price']
    

class Cartitemsserlizer(serializers.ModelSerializer):
    product = simpleproductserlizer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self,cartitem:CartItem):
        return cartitem.quantity * cartitem.product.price

    class Meta:
        model = CartItem
        fields = ['id','product','quantity','total_price']


class cartserilizer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only = True)
    carts = Cartitemsserlizer(many = True,read_only = True)

    total_price = serializers.SerializerMethodField()

    def get_total_price(self,cart:Cart):
        return sum([item.quantity * item.product.price for item in cart.carts.all()])


    class Meta:
        model = Cart
        fields = ['id','carts','total_price']

class getcaritemsermizer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self,value):
        if not Product.objects.filter(pk=value):
            raise serializers.ValidationError('no product exist with this id')
        return value


    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        try:
            cartritem = CartItem.objects.get(cart_id = cart_id,product_id = product_id)
            cartritem.quantity += quantity
            cartritem.save()
            self.instance = cartritem
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id = cart_id,**self.validated_data)
        return self.instance


    class Meta:
        model = CartItem
        fields = ['id','product_id','quantity']

class updatecartitemserlizer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']

    
