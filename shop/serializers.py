from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from shop.models import ProductStoragePrice, ProductPrice


class ProductPriceField(serializers.RelatedField):

    def to_representation(self, value):
        user = self.context['request'].user
        price = value.get_price(user)
        price['quantity'] = value.quantity
        return price



# class PriceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductPrice
#         fields = ('retail_price', 'price_1', 'price_2', 'price_3', 'price_4')


class ProductStoragePriceSerializer(serializers.ModelSerializer):
    price = ProductPriceField(read_only=True)

    class Meta:
        model = ProductStoragePrice
        fields = ('product', 'storage', 'price', 'active', 'added', 'updated')
