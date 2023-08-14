from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer, StringRelatedField, BaseSerializer
from rest_framework import serializers
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

class ImageSerializer(BaseSerializer):
    image = serializers.ImageField(max_length=None, allow_empty_file=False, use_url=True)

    def to_internal_value(self, data):
        img = data.get('image')
        if not img:
            raise serializers.ValidationError({
                'image': 'This field is required.'
            })
        return {
            'image': img
        }

    def to_representation(self, instance):
        return {}
    