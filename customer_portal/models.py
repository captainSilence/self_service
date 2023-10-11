from django.db import models

# Create your models here.
class NewSpeedRequest(models.Model):
    accountNumber = models.CharField(max_length=20)
    customerName = models.TextField(null=True)
    customerType = models.TextField(null=True)
    contractName = models.TextField(null=True)
    contractPhone = models.CharField(max_length=20, null=True)
    contractEmail = models.TextField(null=True)
    currentPlan = models.TextField(null=True)   
    newMRC = models.FloatField(null=True)
    comment = models.TextField(null=True)
    timeCreated = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name + ' ' + str(self.accountNumber)

