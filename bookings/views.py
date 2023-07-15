from django.utils import timezone

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from homestays.models import Service, Homestay
from myadmin.models import PricingConfig
from .models import Booking
from .serializers import BookingSerializer
from users.models import User
from django.http import HttpResponseBadRequest
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from datetime import datetime


@permission_classes([IsAuthenticated])
class BookingList(APIView):

    def get(self, request, username=None):
        # admin get all bookings
        if request.user.is_superuser and request.user.is_staff and not username:
            bookings = Booking.objects.all()
            serializer = BookingSerializer(bookings, many=True)
            return Response(serializer.data)

        # homestay manager get all bookings of his homestays
        if not request.user.is_superuser and request.user.is_staff and username:
            bookings = Booking.objects.filter(homestay__manager_id=request.user)
            serializer = BookingSerializer(bookings, many=True)
            return Response(serializer.data)
        
        # customer get all his bookings
        if not request.user.is_superuser and not request.user.is_staff and request.user.username == username:
            bookings = Booking.objects.filter(user__username=username)
            serializer = BookingSerializer(bookings, many=True)
            return Response(serializer.data)

        return HttpResponseBadRequest('You are not authorized to view this page.')

    def post(self, request, username):
        data = request.data
        user = get_object_or_404(User, username=username)
        data['user'] = user.id

        # only customer can create booking
        if user.is_staff or user.is_superuser:
            return HttpResponseBadRequest('Only customer can create booking.')
        
        service_ids = [service['id'] for service in data.get('services', [])]

        checkin_date = data.get('checkin_date')
        checkout_date = data.get('checkout_date')

        # check valid checkin_date and checkout_date
        if checkin_date and checkout_date:
            checkin_date_dt = datetime.strptime(checkin_date, '%Y-%m-%d')
            checkout_date_dt = datetime.strptime(checkout_date, '%Y-%m-%d')
            if checkin_date_dt >= checkout_date_dt:
                return HttpResponseBadRequest('Checkout date must be later than checkin date.')
            if checkin_date_dt < datetime.now():
                return HttpResponseBadRequest('Checkin date must be later than today.')
            
        # Check if the homestay is occupied
        homestay_id = data.get('homestay')
        if checkin_date and checkout_date and homestay_id:
            existing_bookings = Booking.objects.filter(
                Q(homestay=homestay_id) &
                (~Q(checkout_date__lte=checkin_date) & ~Q(checkin_date__gte=checkout_date))
            )

            if existing_bookings.exists():
                return Response('The homestay is already occupied during the selected dates.', status=status.HTTP_400_BAD_REQUEST)

        # Check maximum adults and maximum children
        num_adults = data.get('num_adults', 0)
        num_children = data.get('num_children', 0)
        homestay = Homestay.objects.get(id=homestay_id)
        max_adults = homestay.max_num_adults
        max_children = homestay.max_num_children
        if num_adults > max_adults:
            max_str = f'The maximum number of adults allowed is {max_adults}.'
            return Response(max_str, status=status.HTTP_400_BAD_REQUEST)
        if num_children > max_children:
            max_str = f'The maximum number of children allowed is {max_children}.'
            return Response(max_str, status=status.HTTP_400_BAD_REQUEST)

        serializer = BookingSerializer(data=data)

        if serializer.is_valid():
            booking = serializer.save()

            # Add services to the booking
            services = Service.objects.filter(id__in=service_ids)
            booking.services.set(services)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Not used
    def delete(self, request, username):
        user = get_object_or_404(User, username=username)
        bookings = Booking.objects.filter(user=user)
        bookings.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookingDetail(APIView):
    def get(self, request, username, booking_id):
        booking = get_object_or_404(Booking, user__username=username, id=booking_id)
        # only booked user, homestay's manager and admin can view the booking
        if not (request.user == booking.user or request.user == booking.homestay.manager_id or request.user.is_superuser):
            return HttpResponseBadRequest('You are not authorized to view this booking.')

        serializer = BookingSerializer(booking)
        return Response(serializer.data)

    def patch(self, request, username, booking_id):
        booking = get_object_or_404(Booking, user__username=username, id=booking_id)
        data = request.data
        data['user'] = booking.user.id

        # Extract only the allowed fields from the data
        allowed_fields = ['comment', 'rating', 'status']
        validated_data = {field: data.get(field) for field in allowed_fields}

        serializer = BookingSerializer(booking, data=validated_data, partial=True)
        if serializer.is_valid():
            updated_booking = serializer.save()

            # Update specific fields if they are present in validated_data
            if 'status' in validated_data and booking.status != validated_data['status']:
                updated_booking.status = validated_data['status']

                if booking.status != "Canceled" and validated_data['status'] == "Canceled":
                    updated_booking.canceled_at = timezone.now()

                    homestay = Homestay.objects.get(id=updated_booking.homestay.id)
                    homestay_price_config = PricingConfig.objects.get(id=homestay.pricing_config_id_id)

                    if (updated_booking.canceled_at.date() - updated_booking.checkin_date).days > homestay_price_config.free_cancellation_days:
                        updated_booking.refund_price = updated_booking.total_price * homestay_price_config.cancellation_refund_percentage
                    else:
                        updated_booking.refund_price = updated_booking.total_price

            if 'comment' in validated_data:
                updated_booking.comment = validated_data['comment']
                updated_booking.review_timestamp = timezone.now()
            if 'rating' in validated_data:
                updated_booking.rating = validated_data['rating']
                updated_booking.review_timestamp = timezone.now()

            updated_booking.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username, booking_id):
        booking = get_object_or_404(Booking, user__username=username, id=booking_id)
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
