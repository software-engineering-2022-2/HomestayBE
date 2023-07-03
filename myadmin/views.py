from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PricingConfig
from .serializers import PricingConfigSerializer


class PricingConfigList(APIView):
    def get(self, request):
        pricing_config = PricingConfig.objects.all()
        serializer = PricingConfigSerializer(pricing_config, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PricingConfigSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self):
        PricingConfig.objects.all().delete()
        return Response(status=204)

class PricingConfigDetail(APIView):
    def get_object(self, pk):
        return PricingConfig.objects.get(pk=pk)

    def get(self, request, pk):
        pricing_config = self.get_object(pk)
        serializer = PricingConfigSerializer(pricing_config)
        return Response(serializer.data)

    def put(self, request, pk):
        pricing_config = self.get_object(pk)
        serializer = PricingConfigSerializer(pricing_config, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, pk):
        print("pk is ", pk)
        pricing_config = self.get_object(pk)
        pricing_config.delete()
        return Response(status=204)

