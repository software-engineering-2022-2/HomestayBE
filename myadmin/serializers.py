from rest_framework.serializers import ModelSerializer
from .models import PricingConfig, ServiceType


class PricingConfigSerializer(ModelSerializer):
    class Meta:
        model = PricingConfig
        fields = '__all__'


class ServiceTypeSerializer(ModelSerializer):
    class Meta:
        model = ServiceType
        fields = '__all__'
