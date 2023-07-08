from django.contrib import admin
from .models import PricingConfig, ServiceType


admin.site.register(PricingConfig)
admin.site.register(ServiceType)
