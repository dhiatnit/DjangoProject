from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import F, Q


class Rides(models.Model):
    rideId = models.AutoField(primary_key=True)

    user = models.ForeignKey("core.User", on_delete=models.CASCADE)
    bike = models.ForeignKey("core.Bikes", on_delete=models.CASCADE)

    startStation = models.ForeignKey(
        "core.Stations",
        on_delete=models.CASCADE,
        related_name="rides_started_here",
    )

    endStation = models.ForeignKey(
        "core.Stations",
        on_delete=models.CASCADE,
        related_name="rides_ended_here",
    )

    startTime = models.DateTimeField()
    endTime = models.DateTimeField()

    distance = models.FloatField(validators=[MinValueValidator(0.0)])

    batteryLevelStart = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    batteryLevelEnd = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(endTime__gt=F("startTime")),
                name="end_after_start",
            ),
            models.CheckConstraint(
                condition=~Q(startStation=F("endStation")),
                name="different_stations",
            ),
        ]

        indexes = [models.Index(fields=["startTime"])]

    def __str__(self):
        return f"Ride {self.rideId}"
