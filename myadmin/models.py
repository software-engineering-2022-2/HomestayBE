from django.db import models


class PricingConfig(models.Model):
    deposit_percentage = models.FloatField()
    cancellation_refund_percentage = models.FloatField()
    free_cancellation_days = models.IntegerField()
    discount = models.FloatField()
