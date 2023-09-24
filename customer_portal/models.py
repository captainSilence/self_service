from django.db import models

# Create your models here.
class NewSpeedRequest(models.Model):
    accountNumber = models.IntegerField()
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phoneNumber = models.CharField(max_length=20)
    newSpeed = models.IntegerField()
    comment = models.CharField(max_length=200, blank=True, default='')
    timeCreated = models.DateTimeField(auto_now_add=True)

