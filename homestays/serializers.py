from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer
from .models import Homestay, Service


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
