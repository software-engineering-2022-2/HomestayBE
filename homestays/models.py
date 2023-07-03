from django.db import models
from django.db import models
import uuid
# Create your models here.
class Homestay(models.Model):

    id = models.UUIDField(primary_key=True, max_length=20, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length= 100)
    price = models.FloatField()
    street_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length= 100)
    availability = models.BooleanField()
    max_num_children = models.IntegerField()
    max_num_adults = models.IntegerField()
    allow_pet = models.BooleanField()
    descrpition = models.CharField(max_length=500)