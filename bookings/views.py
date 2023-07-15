from django.utils import timezone
from django.forms import model_to_dict
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


class BookingList(APIView):
    def get(self, request, username):
        bookings = Booking.objects.filter(user__username=username)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request, username):
        data = request.data
        data['user'] = get_object_or_404(User, username=username).id
        service_ids = [service['id'] for service in data.get('services', [])]

        # Check if the homestay is occupied
        checkin_date = data.get('checkin_date')
        checkout_date = data.get('checkout_date')
        homestay_id = data.get('homestay')
        if checkin_date and checkout_date and homestay_id:
            existing_bookings = Booking.objects.filter(
                Q(homestay=homestay_id) &
                (~Q(checkout_date__lte=checkin_date) & ~Q(checkin_date__gte=checkout_date))
            )

            if existing_bookings.exists():
                return Response('The homestay is already occupied during the selected dates.',
                                status=status.HTTP_400_BAD_REQUEST)

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

    def delete(self, request, username):
        user = get_object_or_404(User, username=username)
        bookings = Booking.objects.filter(user=user)
        bookings.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookingDetail(APIView):
    def get(self, request, username, booking_id):
        user = get_object_or_404(User, username=username)
        booking = get_object_or_404(Booking, user=user, id=booking_id)
        serializer = BookingSerializer(booking)
        return Response(serializer.data)

    def put(self, request, username, booking_id):
        user = get_object_or_404(User, username=username)
        booking = get_object_or_404(Booking, user=user, id=booking_id)
        data = request.data

        # Remove the 'services' field from the data temporarily
        services_data = data.pop('services', [])

        services_data = booking.services.all()

        # Print the services information
        print("Services Information:")
        for service in services_data:
            print("Service ID:", service.id)

        # Update specific fields if they are present in the data
        if 'status' in data and booking.status != data['status']:
            print(booking.status, data['status'])

            if booking.status != "Canceled" and data['status'] == "Canceled":
                booking.canceled_at = timezone.now()

                homestay = Homestay.objects.get(id=booking.homestay.id)
                homestay_price_config = PricingConfig.objects.get(id=homestay.pricing_config_id_id)

                print(booking.canceled_at.date(), booking.checkin_date, homestay_price_config.free_cancellation_days)
                cancel_days = (booking.checkin_date - booking.canceled_at.date()).days
                print(cancel_days)
                if cancel_days < homestay_price_config.free_cancellation_days:
                    booking.refund_price = booking.total_price * homestay_price_config.cancellation_refund_percentage
                else:
                    booking.refund_price = booking.total_price

            booking.status = data['status']

        if 'comment' in data:
            booking.comment = data['comment']
            booking.review_timestamp = timezone.now()
        if 'rating' in data:
            booking.rating = data['rating']
            booking.review_timestamp = timezone.now()

        # Update the related services
        service_ids = [service_data.id for service_data in services_data]
        services = Service.objects.filter(id__in=service_ids)
        booking.services.set(services)

        # Save the booking object
        booking.save()

        serializer = BookingSerializer(booking)

        return Response(serializer.data)

    def delete(self, request, username, booking_id):
        user = get_object_or_404(User, username=username)
        booking = get_object_or_404(Booking, user=user, id=booking_id)
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
