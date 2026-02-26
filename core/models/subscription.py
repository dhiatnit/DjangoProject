
from django.db import models


class Subscription(models.Model):

    class SubscriptionStatus(models.TextChoices):
        ACTIVE = "active"
        INACTIVE = "inactive"

    subscriptionId = models.AutoField(primary_key=True)
    userId = models.ForeignKey("Users", on_delete=models.CASCADE)
    subStatus =models.CharField(max_length=20,choices= SubscriptionStatus.choices)
    startDate = models.DateField()
    endDate = models.DateField()

    def __str__(self):
        return f"user {self.subscriptionId}"


