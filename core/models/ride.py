from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import F, Q


class Ride(models.Model):
    ride_id = models.AutoField(primary_key=True)

    user = models.ForeignKey("core.User", on_delete=models.CASCADE)
    bike = models.ForeignKey("core.bike", on_delete=models.CASCADE)

    start_station = models.ForeignKey(
        "core.station",
        on_delete=models.CASCADE,
        related_name="ride_started_here",
    )

    end_station = models.ForeignKey(
        "core.station",
        on_delete=models.CASCADE,
        related_name="ride_ended_here",
    )

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    distance = models.FloatField(validators=[MinValueValidator(0.0)])

    battery_level_start = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    battery_level_end = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(end_time__gt=F("start_time")),
                name="end_after_start",
            ),
            models.CheckConstraint(
                condition=~Q(start_station=F("end_station")),
                name="different_station",
            ),
        ]

        indexes = [models.Index(fields=["start_time"])]

    def __str__(self):
        return f"Ride {self.ride_id}"
