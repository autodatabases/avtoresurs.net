import json

from django.utils.formats import number_format
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault, DecimalField

from shop.models import ProductPrice


class ProductPriceField(serializers.RelatedField):
    def to_representation(self, value):
        user = self.context['request'].user
        price = value.get_price(user)
        price['quantity'] = value.quantity
        return price


class ProductPriceSerializer(serializers.ModelSerializer):
    # price = ProductPriceField(read_only=True)
    whosale_price = serializers.SerializerMethodField()

    def get_whosale_price(self, obj):
        user = self.context['request'].user
        whosale_price = obj.get_whosale_price(user)
        return number_format(whosale_price)

    class Meta:
        model = ProductPrice
        fields = ('product', 'storage', 'quantity', 'retail_price', 'whosale_price', 'added', 'updated')
