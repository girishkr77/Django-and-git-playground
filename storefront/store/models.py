from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from uuid import uuid4

class Promotions (models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
    

class Collection (models.Model):
    title = models.CharField(max_length=255)
    feature_product = models.ForeignKey('Product',on_delete=models.SET_NULL,null=True,related_name='+')

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']


class Product (models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(null=True,blank=True)
    price = models.DecimalField(
                                max_digits=6
                                ,decimal_places=2
                                ,validators=[MinValueValidator(1)])
    inventory = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT,default='1',related_name='products')
    promotions = models.ManyToManyField(Promotions,blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Customer (models.Model):
    MEMBERSHIP_BROWNZ = 'B'
    MEMBERSHIP_SLIVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMNERSHIP_CHOICES = [
        (MEMBERSHIP_BROWNZ,'BROWNZ'),
        (MEMBERSHIP_SLIVER,'SLIVER'),
        (MEMBERSHIP_GOLD,'GOLD')

    ]
    email = models.EmailField(unique=True, null=True)
    phone = models.CharField(max_length=255,null=True)
    birth_date = models.DateField(null=True)
    member_ship = models.CharField(max_length=1,choices=MEMNERSHIP_CHOICES,default=MEMBERSHIP_BROWNZ)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    def first_name(self):
        return self.user.first_name
    
    def last_name(self):
        return self.user.last_name
    
    class Meta:
        ordering = ['user__first_name','user__last_name']
        permissions = [
            ('view_history','can view history')
        ]

class Order (models.Model):
    PAYMENT_PENDING = 'P'
    PAYMENT_COMPLETED = 'C'
    PAYMENT_FAILED = 'F'
    
    PAYMENT_LIST = [
        (PAYMENT_PENDING,'PENDING'),
        (PAYMENT_COMPLETED,'COMPLETED'),
        (PAYMENT_FAILED,'FAILED')
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1,choices=PAYMENT_LIST,default=PAYMENT_PENDING)
    customer = models.ForeignKey(Customer,on_delete=models.PROTECT)

    class Meta:
        permissions = [
            ('cancel_order','can cancel the order')
        ]
    

class Address (models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    zip = models.CharField(max_length=255)
    class Meta:
        db_table = 'store_addressgnf'
    

class OrderItem (models.Model):
    order = models.ForeignKey(Order,on_delete=models.PROTECT,related_name='orderitems')
    quantity = models.PositiveSmallIntegerField()
    product = models.ForeignKey(Product,on_delete=models.PROTECT,related_name='product')
    item_prize = models.DecimalField(max_digits=6,decimal_places=2)


class Cart (models.Model):
    id = models.UUIDField(primary_key=True,default=uuid4)
    created_date = models.DateTimeField(auto_now_add=True)


class CartItem (models.Model):
    quantity = models.PositiveSmallIntegerField(validators = [MinValueValidator(1)])
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,related_name='carts')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    itemprice = models.DecimalField(max_digits=6,decimal_places=2)

    class Meta:
        unique_together = [['cart','product']]

class Review (models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)

