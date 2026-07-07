from decimal import Decimal
from rest_framework import serializers

from store.models import Product

class productSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    unit_price = serializers.DecimalField(max_digits=6,decimal_places=2, source = 'price')
    tax_price = serializers.SerializerMethodField(method_name='tax_calculated')

    def tax_calculated(seld,product:Product):
        return product.price*Decimal(1.1)