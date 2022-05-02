from django.db import models

# Create your models here.
class Profile(models.Model):
    name = models.CharField(null=False, max_length=100)
    tether_balance = models.FloatField(default=0)
    bitcoin_balance = models.FloatField(default=0)