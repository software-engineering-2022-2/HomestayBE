from django.db import models
from enum import Enum
from django.utils import timezone
from homestays.models import Service, Homestay
from myadmin.models import PricingConfig
from django.core.exceptions import ValidationError


class BookingStatus(Enum):
    PENDING = 'Pending'
    CONFIRMED = 'Confirmed'
    COMPLETED = 'Completed'
    CANCELED = 'Canceled'
    REFUNDED = 'Refunded'


class Booking(models.Model):
    checkin_date = models.DateTimeField(null=True)
    checkout_date = models.DateTimeField(null=True)
    num_adults = models.IntegerField(null=True)
    canceled_at = models.DateTimeField(blank=True, null=True)
    total_price = models.FloatField(blank=True, null=True)
    deposit_price = models.FloatField(blank=True, null=True)
    refund_price = models.FloatField(blank=True, null=True)
    comment = models.CharField(max_length=200, blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    review_timestamp = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[(status.name, status.value) for status in BookingStatus],
        default=BookingStatus.PENDING.value
    )
    created_at = models.DateTimeField(auto_now_add=True)
    num_children = models.IntegerField(default=0, null=True)
    services = models.ManyToManyField(Service)
    homestay = models.ForeignKey(Homestay, on_delete=models.CASCADE)

    def update_total_price(self):
        homestay = Homestay.objects.get(id=self.homestay.id)
        homestay_price = homestay.price
        homestay_price_config = PricingConfig.objects.get(id=homestay.pricing_config_id)
        total_price = homestay_price + sum(service.price for service in self.services.all())
        if homestay_price_config.discount > 0:
            total_price = total_price * (1 - homestay_price_config.discount)
        self.total_price = total_price
        self.deposit_price = total_price * homestay_price_config.deposit_percentage

    def save(self, *args, **kwargs):
        self.update_total_price()

        if self.pk is not None:
            original_booking = Booking.objects.get(pk=self.pk)
            if original_booking.status != BookingStatus.CANCELED.name and self.status == BookingStatus.CANCELED.name:
                self.canceled_at = timezone.now()

                homestay = Homestay.objects.get(id=self.homestay.id)
                homestay_price_config = PricingConfig.objects.get(id=homestay.pricing_config_id)

                if (self.canceled_at.date() - self.checkin_date.date()).days > homestay_price_config.free_cancellation_days:
                    self.refund_price = self.total_price * homestay_price_config.cancellation_refund_percentage
                else:
                    self.refund_price = self.total_price

        super().save(*args, **kwargs)

    def clean(self):
        if self.num_adults > self.homestay.max_num_adults:
            raise ValidationError("Number of adults exceeds the maximum limit for this homestay.")

        if self.num_children > self.homestay.max_num_children:
            raise ValidationError("Number of children exceeds the maximum limit for this homestay.")
