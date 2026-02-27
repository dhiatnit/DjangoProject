from django.db import models
from django.db.models import Q


class Payment(models.Model):
    paymentId = models.AutoField(primary_key=True)
    subscriptionId = models.ForeignKey("core.Subscription", on_delete=models.CASCADE)
    rideId = models.ForeignKey("core.Rides", on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=20)
    method = models.CharField(max_length=100)
    payStatus = models.CharField(max_length=100)

    def __str__(self):
        return f"user {self.paymentId}"

    class Meta:
        indexes = [
            models.Index(fields=["subscriptionId"]),
            models.Index(fields=["rideId"]),
            models.Index(fields=["payStatus"]),
            models.Index(fields=["method"]),
        ]

        constraints = [
            models.CheckConstraint(
                condition=Q(amount__gt=0),
                name="payment_amount_positive",
            ),
        ]
