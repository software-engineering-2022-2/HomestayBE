from django.db import models
from enum import Enum
from django.utils import timezone
from homestays.models import Service, Homestay
from myadmin.models import PricingConfig
from django.core.exceptions import ValidationError
from users.models import User
import datetime


# PENDING = 'Pending'
# CONFIRMED = 'Confirmed'
# COMPLETED = 'Completed'
# CANCELED = 'Canceled'
# REFUNDED = 'Refunded'

class Booking(models.Model):
    checkin_date = models.DateField(null=True)
    checkout_date = models.DateField(null=True)
    num_adults = models.IntegerField(null=True)
    canceled_at = models.DateTimeField(blank=True, null=True)
    total_price = models.FloatField(blank=True, null=True)
    deposit_price = models.FloatField(blank=True, null=True)
    refund_price = models.FloatField(blank=True, null=True)
    comment = models.CharField(max_length=200, blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    review_timestamp = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20,default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    num_children = models.IntegerField(default=0, null=True)
    services = models.ManyToManyField(Service)
    homestay = models.ForeignKey(Homestay, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def update_total_deposit_price(self):
        homestay = Homestay.objects.get(id=self.homestay.id)
        homestay_price = homestay.price
        homestay_price_config = PricingConfig.objects.get(id=homestay.pricing_config_id_id)
        checkin_date_dt = datetime.datetime.strptime(str(self.checkin_date), '%Y-%m-%d')
        checkout_date_dt = datetime.datetime.strptime(str(self.checkout_date), '%Y-%m-%d')
        total_price = homestay_price*(checkout_date_dt - checkin_date_dt).days + sum(service.price for service in self.services.all())
        if homestay_price_config.discount > 0:
            total_price = total_price * (1 - homestay_price_config.discount)
        self.total_price = total_price
        self.deposit_price = total_price * homestay_price_config.deposit_percentage
        self.save()
