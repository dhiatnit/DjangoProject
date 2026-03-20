from django.db import models
from django.db.models import F, Q


class Subscription(models.Model):
    class SubscriptionStatus(models.TextChoices):
        ACTIVE = "active"
        INACTIVE = "inactive"
        PENDING = "pending"

    subscription_id = models.AutoField(primary_key=True)
    user = models.ForeignKey("core.User", on_delete=models.CASCADE)
    sub_status = models.CharField(max_length=20, choices=SubscriptionStatus.choices)
    start_date = models.DateField()
    end_date = models.DateField()
    subscription_plan = models.ForeignKey("core.subscriptionPlan", on_delete=models.CASCADE)

    def __str__(self):
        return f"user {self.subscription_id}"

    class Meta:
        indexes = [

            models.Index(fields=["sub_status"]),
            models.Index(fields=["start_date"]),
            models.Index(fields=["end_date"]),

        ]

        constraints = [
            models.CheckConstraint(
                condition=Q(start_date__lt=F("end_date")),
                name="subscription_start_before_end",
            ),
            models.UniqueConstraint(
                fields=["user", "start_date", "end_date"],
                name="unique_user_subscription_period",
            ),
        ]
