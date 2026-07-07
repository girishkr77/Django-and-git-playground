from django.core.validators import MinValueValidator
from django.db import models

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
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT,default='1')
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
    first_name = models.CharField(max_length=255)
    Last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    member_ship = models.CharField(max_length=1,choices=MEMNERSHIP_CHOICES,default=MEMBERSHIP_BROWNZ)

    def __str__(self):
        return f'{self.first_name} {self.Last_name}'
    
    class Meta:
        ordering = ['first_name','Last_name']

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
    

class Address (models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    zip = models.CharField(max_length=255)
    class Meta:
        db_table = 'store_addressgnf'
    

class OrderItem (models.Model):
    order = models.ForeignKey(Order,on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    product = models.ForeignKey(Product,on_delete=models.PROTECT)
    item_prize = models.DecimalField(max_digits=6,decimal_places=2)


class Cart (models.Model):
    creted_date = models.DateTimeField(auto_now_add=True)

class CartItem (models.Model):
    quantity = models.PositiveSmallIntegerField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
