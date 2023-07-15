from django.db import models
from cloudinary.models import CloudinaryField

import uuid


class Homestay(models.Model):

    id = models.UUIDField(primary_key=True, max_length=20, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length= 100)
    price = models.FloatField()
    description = models.TextField()
    max_num_adults = models.IntegerField()
    max_num_children = models.IntegerField()
    allow_pet = models.BooleanField()
    availability = models.BooleanField()
    street_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    manager_id = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True)
    pricing_config_id = models.ForeignKey('myadmin.PricingConfig', on_delete=models.CASCADE, null=True)
    image = CloudinaryField('image', blank=True, null=True)

    def __str__(self):
        return self.name

class Service(models.Model):

    price = models.FloatField()
    description = models.TextField()
    availability = models.BooleanField()
    service_type_id = models.ForeignKey('myadmin.ServiceType', on_delete=models.CASCADE)
    homestay_id = models.ForeignKey('Homestay', on_delete=models.CASCADE)

    def __str__(self):
        return self.description
