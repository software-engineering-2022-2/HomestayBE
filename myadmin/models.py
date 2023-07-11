from django.db import models


class PricingConfig(models.Model):
    name = models.CharField(max_length=100, default="")
    deposit_percentage = models.FloatField()
    cancellation_refund_percentage = models.FloatField()
    free_cancellation_days = models.IntegerField()
    discount = models.FloatField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.name == "":
            self.name = f"price config {self.id}"
            self.save()

    def __str__(self):
        return self.name


class ServiceType(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name
