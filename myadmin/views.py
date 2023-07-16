from django.shortcuts import render, get_object_or_404

from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly

from .models import PricingConfig, ServiceType
from .serializers import PricingConfigSerializer, ServiceTypeSerializer


# @permission_classes([IsAdminUser])
class PricingConfigList(APIView):
    
    def get(self, request):
        pricing_config = PricingConfig.objects.all()
        serializer = PricingConfigSerializer(pricing_config, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Only admin can create pricing_config
        if not request.user.is_superuser:
            return Response(status=403, data={'detail': 'Only admin can create pricing_config'})
        
        serializer = PricingConfigSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, request):
        # Only admin can delete all pricing_config
        if not request.user.is_superuser:
            return Response(status=403, data={'detail': 'Only admin can delete all pricing_config'})
        
        PricingConfig.objects.all().delete()
        return Response(status=204)


@permission_classes([IsAuthenticatedOrReadOnly])
class PricingConfigDetail(APIView):
    
    def get_object(self, pk):
        return get_object_or_404(PricingConfig, pk=pk)

    def get(self, request, pk):
        pricing_config = self.get_object(pk)
        serializer = PricingConfigSerializer(pricing_config)
        return Response(serializer.data)

    def put(self, request, pk):
        # Only admin can update pricing_config
        if not request.user.is_superuser:
            return Response(status=403, data={'detail': 'Only admin can update pricing_config'})
        
        pricing_config = self.get_object(pk)
        serializer = PricingConfigSerializer(pricing_config, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, pk):
        # Only admin can delete pricing_config
        if not request.user.is_superuser:
            return Response(status=403, data={'detail': 'Only admin can delete pricing_config'})
        
        pricing_config = self.get_object(pk)
        pricing_config.delete()
        return Response(status=204)


@permission_classes([IsAdminUser])
class ServiceTypeList(APIView):

    def get(self, request):
        service_type = ServiceType.objects.all()
        serializer = ServiceTypeSerializer(service_type, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Only admin can create service_type
        if not request.user.is_superuser:
            return Response(status=403, data={'detail': 'Only admin can create service_type'})
        
        serializer = ServiceTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
        
    def delete(self, request):
        # Only admin can delete all service_type
        if not request.user.is_superuser:
            return Response(status=403, data={'detail': 'Only admin can delete all service_type'})
        
        ServiceType.objects.all().delete()
        return Response(status=204)


@permission_classes([IsAuthenticatedOrReadOnly])
class ServiceTypeDetail(APIView):

    def get_object(self, pk):
        return get_object_or_404(ServiceType, pk=pk)

    def get(self, request, pk):
        service_type = self.get_object(pk)
        serializer = ServiceTypeSerializer(service_type)
        return Response(serializer.data)

    def put(self, request, pk):
        # Only admin can update service_type
        if not request.user.is_superuser:
            return Response(status=403, data={'detail': 'Only admin can update service_type'})
        
        service_type = self.get_object(pk)
        serializer = ServiceTypeSerializer(service_type, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, pk):
        # Only admin can delete service_type
        if not request.user.is_superuser:
            return Response(status=403, data={'detail': 'Only admin can delete service_type'})
        
        service_type = self.get_object(pk)
        service_type.delete()
        return Response(status=204)
