from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.endpoints),
    path('homestay/', views.ListHomestays.as_view(), name='homestay'),
    path('homestay/<str:name>/', views.ListHomestays.as_view(), name='homestay_detail'),
]
