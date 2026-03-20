from django.db import models
from django.db.models import Q


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    subscription = models.ForeignKey("core.Subscription",  on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='payments')
    ride = models.ForeignKey("core.ride",on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='payments',)
    amount = models.DecimalField(decimal_places=2, max_digits=20)
    method = models.CharField(max_length=100)
    pay_status = models.CharField(max_length=100)
    payment_time = models.DateTimeField()

    def __str__(self):
        return f"user {self.payment_id}"

    class Meta:
        indexes = [
            models.Index(fields=['pay_status']),
            models.Index(fields=['method']),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(amount__gt=0),
                name='payment_amount_positive',
            ),
            models.CheckConstraint(
                condition=(
                        (Q(ride__isnull=False) & Q(subscription__isnull=True)) |
                        (Q(ride__isnull=True) & Q(subscription__isnull=False))
                ),
                name='payment_for_ride_xor_subscription',
            ),
        ]