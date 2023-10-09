from django.db import models

# Create your models here.
class NewSpeedRequest(models.Model):
    accountNumber = models.CharField(max_length=20)
    nodeID = models.IntegerField(null=True)
    customerName = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=20, null=True)
    customerType = models.CharField(max_length=100, null=True)
    productOffer = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=500)
    address = models.CharField(max_length=500, null=True)
    MRC = models.FloatField(null=True)
    timeCreated = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name + ' ' + str(self.accountNumber)

