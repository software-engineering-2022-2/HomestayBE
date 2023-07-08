from django.urls import path
from . import views

urlpatterns = [
    path('pricing_configs/', views.PricingConfigList.as_view(), name='pricing_config_list'),
    path('pricing_configs/<int:pk>/', views.PricingConfigDetail.as_view(), name='pricing_config_detail'),
    path('service_types/', views.ServiceTypeList.as_view(), name='service_type_list'),
    path('service_types/<int:pk>/', views.ServiceTypeDetail.as_view(), name='service_type_detail'),
]