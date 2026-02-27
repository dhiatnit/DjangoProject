from django.db import models


class Subscription(models.Model):
    class SubscriptionStatus(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"

    subscriptionId = models.AutoField(primary_key=True)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    subStatus = models.CharField(max_length=20, choices=SubscriptionStatus.choices)
    startDate = models.DateField()
    endDate = models.DateField()

    def __str__(self):
        return f"subscription {self.subscriptionId}"
