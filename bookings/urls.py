from django.urls import path
from . import views


urlpatterns = [
    path('bookings/', views.BookingList.as_view(), name='all_bookings'),
    path('bookings/<str:username>/', views.BookingList.as_view(), name='booking'),
    path('bookings/<str:username>/<str:booking_id>/', views.BookingDetail.as_view(), name='booking_detail'),
]
