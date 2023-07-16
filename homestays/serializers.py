from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer, StringRelatedField
from .models import Homestay, Service
from myadmin.serializers import ServiceTypeSerializer, PricingConfigSerializer


class HomestaySerializer(ModelSerializer):
    class Meta:
        model = Homestay
        fields = '__all__'

    def validate_password(self, value: str) -> str:
        return make_password(value)
    
class HomestayGetSerializer(ModelSerializer):
    pricing_config = PricingConfigSerializer(read_only = True)
    class Meta:
        model = Homestay
        fields = '__all__'

class ServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
    
class ServiceGetSerializer(ModelSerializer):
    service_type = ServiceTypeSerializer(read_only = True)
    class Meta:
        model = Service
        fields = ['id', 'price', 'description', 'availability', 'service_type_id', 'service_type', 'homestay_id']
