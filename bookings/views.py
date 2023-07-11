from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics
from .models import Booking
from .serializers import BookingSerializer


class BookingList(generics.ListCreateAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)
        return Booking.objects.filter(user=user)

    def perform_create(self, serializer):
        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)
        serializer.save(user=user)


class BookingDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)
        return Booking.objects.filter(user=user)

    def get_object(self):
        queryset = self.get_queryset()
        booking_id = self.kwargs['booking_id']
        return get_object_or_404(queryset, id=booking_id)
