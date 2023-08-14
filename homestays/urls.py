from django.urls import path
from . import views


urlpatterns = [
    path('homestays/', views.ListHomestays.as_view(), name='homestay'),
    path('homestays/<str:homestay_id>/', views.HomestayDetail.as_view(), name='homestay_detail'),
    path('homestays/<str:homestay_id>/image/', views.HomestayUpdateImage.as_view(), name='homestay_image'),
    path('homestays/<str:homestay_id>/services/', views.ListServices.as_view(), name='service'),
    path('homestays/services/<int:service_id>/', views.ServiceDetail.as_view(), name='service_detail')
]
