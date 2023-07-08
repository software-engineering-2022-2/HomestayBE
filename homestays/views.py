from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Homestay
from .serializers import HomestaySerializer
from django.db.models import Q


# @permission_classes([IsAuthenticatedOrReadOnly])
class ListHomestays(APIView):

    def get(self, request):
        query_name = request.GET.get('name', '').strip()
        query_city = request.GET.get('city', '').strip()
        if query_name:
            homestays = Homestay.objects.filter(name__icontains=query_name)
        elif query_city:
            homestays = Homestay.objects.filter(city__icontains=query_city)
        else:
            homestays = Homestay.objects.all()
        
        serializer = HomestaySerializer(homestays, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Only admin can create homestays
        if not request.user.is_superuser:
            return Response(status=403, data={'detail': 'Only admin can create homestays'})
        
        serializer = HomestaySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
        
    def delete(self, request):
        # Only admin can delete all homestays
        if not request.user.is_superuser:
            return Response(status=403, data={'detail': 'Only admin can delete all homestays'})
        
        Homestay.objects.all().delete()
        return Response(status=204)


@permission_classes([IsAuthenticatedOrReadOnly])
class HomestayDetail(APIView):

    def get_object(self, homestay_id):
        return get_object_or_404(Homestay, id=homestay_id)

    def get(self, request, homestay_id):
        homestay = self.get_object(homestay_id)
        serializer = HomestaySerializer(homestay)
        return Response(serializer.data)

    def put(self, request, homestay_id):
        # Only admin and homestay manager can update homestays
        if not request.user.is_staff:
            return Response(status=403, data={'detail': 'You do not have permission to update homestays'})

        homestay = self.get_object(homestay_id)
        serializer = HomestaySerializer(homestay, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, homestay_id):
        # Only admin can delete homestays
        if not request.user.is_superuser:
            return Response(status=403, data={'detail': 'Only admin can delete homestays'})
        
        homestay = self.get_object(homestay_id)
        homestay.delete()
        return Response(status=204)
