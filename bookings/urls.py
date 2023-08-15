from django.urls import path
from . import views


urlpatterns = [
    path('bookings/', views.BookingList.as_view(), name='all_bookings'),
    path('bookings/booked_dates/<homestay_id>/', views.BookedDates.as_view(), name='free_dates'),
    path('bookings/<str:username>/', views.BookingList.as_view(), name='booking'),
    path('bookings/<str:username>/analytics/', views.BookingAnalytics.as_view(), name='booking_analytics'),
    path('bookings/<str:username>/<str:booking_id>/', views.BookingDetail.as_view(), name='booking_detail'),
]
