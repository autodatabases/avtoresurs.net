from rest_framework.generics import RetrieveAPIView, ListAPIView
from shop.models import ProductPrice
from shop.serializers import ProductPriceSerializer


class PPList(ListAPIView):
    queryset = ProductPrice.objects.all()[:10]
    serializer_class = ProductPriceSerializer


class PPDedail(RetrieveAPIView):
    queryset = ProductPrice.objects.all()
    serializer_class = ProductPriceSerializer