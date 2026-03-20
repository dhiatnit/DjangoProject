from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q

from .choices import BikeStatus, BikeType


class Bike(models.Model):
    bike_id = models.AutoField(primary_key=True)
    station = models.ForeignKey("core.station",  on_delete=models.SET_NULL,
        null=True,
        blank=True )
    bike_type = models.CharField(max_length=20)
    model = models.CharField(max_length=120)
    battery_level = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True
    )
    bike_status = models.CharField(max_length=20, choices=BikeStatus.choices, default=BikeStatus.AVAILABLE)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=(
                        Q(bike_type=BikeType.ELECTRIC, battery_level__isnull=False)
                        | Q(bike_type=BikeType.NON_ELECTRIC, battery_level__isnull=True)
                ),
                name="battery_consistency_for_each_type",
            ),

            models.CheckConstraint(
                condition=(
                    Q(bike_status=BikeStatus.AVAILABLE, station__isnull=False)
                    | Q(bike_status=BikeStatus.NOT_AVAILABLE, station__isnull=True)
                ),
                name="bike_station_consistency",
            ),
        ]
        indexes = [

            models.Index(fields=["bike_status"]),
        ]
    def __str__(self):
        return f"Bike {self.bike_id}"
