from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer, StringRelatedField
from .models import Homestay, Service
from myadmin.serializers import ServiceTypeSerializer


class HomestaySerializer(ModelSerializer):
    class Meta:
        model = Homestay
        fields = '__all__'

    def validate_password(self, value: str) -> str:
        return make_password(value)


class ServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
    
class ServiceGetSerializer(ModelSerializer):
    service_type = ServiceTypeSerializer(read_only = True)
    class Meta:
        model = Service
        fields = ['price', 'description', 'availability', 'service_type_id', 'service_type', 'homestay_id']
