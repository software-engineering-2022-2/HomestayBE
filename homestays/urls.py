from django.urls import path
from . import views


urlpatterns = [
    path('homestays/', views.ListHomestays.as_view(), name='homestay'),
    path('homestays/<str:homestay_id>/', views.HomestayDetail.as_view(), name='homestay_detail'),
]
