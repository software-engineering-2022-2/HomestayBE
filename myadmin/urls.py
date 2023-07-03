from django.urls import path
from . import views

urlpatterns = [
    path('pricing_configs/', views.PricingConfigList.as_view(), name='pricing_config_list'),
    path('pricing_configs/<int:pk>/', views.PricingConfigDetail.as_view(), name='pricing_config_detail')
]