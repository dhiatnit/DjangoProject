from django.db import models


class SubscriptionPlan(models.Model):
    subscription_plan_id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=100, unique=True )

    cost = models.DecimalField( max_digits=8, decimal_places=2)

    duration = models.PositiveIntegerField()

    is_active = models.BooleanField( default=True )

    class Meta:

        indexes = [

            models.Index(fields=["is_active"]),
        ]

        constraints = [
            models.CheckConstraint(
                condition=models.Q(cost__gte=0),
                name="cost_non_negative"
            ),
            models.CheckConstraint(
                condition=models.Q(duration__gt=0),
                name="duration_positive"
            ),
        ]

    def __str__(self):
        return self.name