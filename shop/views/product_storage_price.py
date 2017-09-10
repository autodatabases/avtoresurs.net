from django.http import JsonResponse, Http404
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework.generics import RetrieveAPIView, ListAPIView

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from shop.models import ProductStoragePrice
from shop.serializers import ProductStoragePriceSerializer




class PSPList(ListAPIView):
    queryset = ProductStoragePrice.objects.all()[:10]
    serializer_class = ProductStoragePriceSerializer





# @permission_classes((permissions.AllowAny,))
# class PSPList(APIView):
#     def get(self, request, format=None):
#         psp = ProductStoragePrice.objects.all()[:10]
#         serializer = ProductStoragePriceSerializer(psp, many=True)
#         return Response(serializer.data)



class PSPDetail(RetrieveAPIView):
    queryset = ProductStoragePrice.objects.all()
    serializer_class = ProductStoragePriceSerializer


    def get(self, request, *args, **kwargs):
        context = super(PSPDetail, self).get(self.request)
        return context