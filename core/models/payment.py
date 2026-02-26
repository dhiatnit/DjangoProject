from django.db import models

from core.models.subscription import Subscription
from core.models.rides import Ride


class Payment(models.Model):
    paymentId = models.AutoField(primary_key=True)
    subscriptionId = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    rideId = models.ForeignKey(Ride, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=20)
    method = models.CharField(max_length=100)
    payStatus = models.CharField(max_length=100)

    def __str__(self):
        return f"user {self.paymentId}"