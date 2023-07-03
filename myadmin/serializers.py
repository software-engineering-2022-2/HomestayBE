from rest_framework.serializers import ModelSerializer
from .models import PricingConfig


class PricingConfigSerializer(ModelSerializer):
    class Meta:
        model = PricingConfig
        fields = '__all__'