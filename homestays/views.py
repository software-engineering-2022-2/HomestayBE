from django.shortcuts import get_object_or_404
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Homestay, Service
from .serializers import HomestaySerializer, ServiceSerializer, ServiceGetSerializer
from django.db.models import Q
from myadmin.models import ServiceType


@permission_classes([IsAuthenticatedOrReadOnly])
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
        bookings = homestay.booking_set.all()

        reviews = []
        for booking in bookings:
            if booking.comment and booking.rating and booking.review_timestamp:
                reviews.append({
                    'comment': booking.comment,
                    'rating': booking.rating,
                    'review_timestamp': booking.review_timestamp,
                    'user': {
                        'first_name': booking.user.first_name,
                        'last_name': booking.user.last_name,
                    }
                })
        reviews.sort(key=lambda x: x['review_timestamp'], reverse=True)
        avg_rating = None if len(reviews) == 0 else sum(int(review['rating']) for review in reviews) / len(reviews)

        serializer = HomestaySerializer(homestay)
        data = serializer.data
        data['reviews'] = reviews
        data['avg_rating'] = avg_rating

        return Response(data)

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


@permission_classes([IsAuthenticatedOrReadOnly])
class ListServices(APIView):

    def get(self, request, homestay_id):
        homestay = get_object_or_404(Homestay, id=homestay_id)
        services = homestay.service_set.all()
        for service in services:
            service.service_type = get_object_or_404(ServiceType, id=service.service_type_id_id)
        serializer = ServiceGetSerializer(services, many=True)
        return Response(serializer.data)
    
    def post(self, request, homestay_id):
        if not request.user.is_staff:
            return Response(status=403, data={'detail': 'You do not have permission to create services'})
        
        serializer = ServiceSerializer(data=request.data)
        serializer.initial_data['homestay_id'] = homestay_id
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, homestay_id):
        if not request.user.is_staff:
            return Response(status=403, data={'detail': 'You do not have permission to delete services'})
        
        homestay = get_object_or_404(Homestay, id=homestay_id)
        homestay.service_set.all().delete()
        return Response(status=204)


@permission_classes([IsAuthenticatedOrReadOnly])
class ServiceDetail(APIView):

    def get_object(self, service_id):
        return get_object_or_404(Service, id=service_id)

    def get(self, request, service_id):
        service = self.get_object(service_id)
        serializer = ServiceSerializer(service)
        return Response(serializer.data)

    def put(self, request, service_id):
        if not request.user.is_staff:
            return Response(status=403, data={'detail': 'You do not have permission to update services'})

        service = self.get_object(service_id)
        serializer = ServiceSerializer(service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, service_id):
        if not request.user.is_staff:
            return Response(status=403, data={'detail': 'You do not have permission to delete services'})
        
        service = self.get_object(service_id)
        service.delete()
        return Response(status=204)
