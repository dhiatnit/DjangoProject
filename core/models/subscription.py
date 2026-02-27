
from django.db import models
from django.db.models import F, Q


class Subscription(models.Model):

    class SubscriptionStatus(models.TextChoices):
        ACTIVE = "active"
        INACTIVE = "inactive"

    subscriptionId = models.AutoField(primary_key=True)
    userId = models.ForeignKey("User", on_delete=models.CASCADE)
    subStatus =models.CharField(max_length=20,choices= SubscriptionStatus.choices)
    startDate = models.DateField()
    endDate = models.DateField()

    def __str__(self):
        return f"user {self.subscriptionId}"

    class Meta:
        indexes = [
            models.Index(fields=['userId']),  # FK index
            models.Index(fields=['subStatus']),  # filtering by status
            models.Index(fields=['startDate']),
            models.Index(fields=['endDate']),
            models.Index(fields=['userId', 'startDate']),  # composite
        ]

        constraints = [
            # Ensure startDate < endDate
            models.CheckConstraint(
                check=Q(startDate__lt=F('endDate')),
                name='subscription_start_before_end'
            ),

            # Prevent duplicate identical subscriptions
            models.UniqueConstraint(
                fields=['userId', 'startDate', 'endDate'],
                name='unique_user_subscription_period'
            ),
        ]