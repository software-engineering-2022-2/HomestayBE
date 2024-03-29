from django.shortcuts import get_object_or_404
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Homestay, Service
from .serializers import HomestaySerializer, ServiceSerializer, ServiceGetSerializer, HomestayGetSerializer, ImageSerializer
from django.db.models import Q
from myadmin.models import ServiceType, PricingConfig
import math
from cloudinary.models import CloudinaryResource
from cloudinary.uploader import upload, destroy
from cloudinary.utils import cloudinary_url
import cloudinary


PAGE_SIZE = 8


@permission_classes([IsAuthenticatedOrReadOnly])
class ListHomestays(APIView):

    def get(self, request):
        query_name = request.GET.get('name', '').strip()
        query_city = request.GET.get('city', '').strip()
        page = int(request.GET.get('page', '0'))
        # TODO: check page range.

        query_manager = request.GET.get('manager', '').strip()
        if query_manager:
            homestays = Homestay.objects.filter(manager_id=query_manager)
        elif query_name:
            homestays = Homestay.objects.filter(name__icontains=query_name)
        elif query_city:
            homestays = Homestay.objects.filter(city__icontains=query_city)
        else:
            homestays = Homestay.objects.all()
        
        max_page =  math.ceil(len(homestays) / PAGE_SIZE) 
        
        homestays = homestays[PAGE_SIZE * page: PAGE_SIZE * (page + 1)]
        
        serializer = HomestaySerializer(homestays, many=True)

        # calculate average rating for each homestay
        data = []
        for homestay_serialied, homestay in zip(serializer.data, homestays):
            bookings = homestay.booking_set.all()
            ratings = []
            for booking in bookings:
                if booking.rating:
                    ratings.append(booking.rating)
            avg_rating = None if len(ratings) == 0 else sum(ratings) / len(ratings)
            homestay_serialied['avg_rating'] = avg_rating
            data.append(homestay_serialied)
        
        # sort homestays by average rating, leave the null ratings at the end
        data.sort(key=lambda x: x['avg_rating'] if x['avg_rating'] else -1, reverse=True)

        return Response({'data': data, 'max_page': max_page, 'current_page': page})
    
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
        homestay.pricing_config = PricingConfig.objects.get(pk = homestay.pricing_config_id_id)
        serializer = HomestayGetSerializer(homestay)
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

@permission_classes([IsAuthenticated])
class HomestayUpdateImage(APIView):

    def put(self, request, homestay_id):
        serializer = ImageSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        homestay = get_object_or_404(Homestay, id=homestay_id)

        # Remove old image if it exists
        if homestay.image:
            public_id = homestay.image.public_id
            destroy(public_id)

        # Upload new image
        image = serializer.validated_data.get('image')
        upload_result = upload(image, folder='homestay-renting-website/homestays')
        url, options = cloudinary_url(upload_result['public_id'],
                                      format=upload_result['format'])
        homestaySerializer = HomestaySerializer(homestay, data={"image": url}, partial=True)
        
        if not homestaySerializer.is_valid():
            return Response(homestaySerializer.errors, status=400)
        homestaySerializer.save()
        return Response(homestaySerializer.data, status=200)
        


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
