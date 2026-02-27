from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .choices import BikeType


class Stations(models.Model):
    station_id = models.AutoField(primary_key=True)
    zone = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)])
    address = models.CharField(max_length=255)

    class Meta:
        indexes = [models.Index(fields=["zone"])]

    def __str__(self):
        return f"Station {self.station_id} - Zone {self.zone}"


class StationCapacity(models.Model):
    station = models.ForeignKey("core.Stations", on_delete=models.CASCADE, related_name="capacities")
    bike_type = models.CharField(max_length=20, choices=BikeType.choices)
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["station", "bike_type"], name="unique_station_biketype")
        ]

    def __str__(self):
        return f"{self.station} - {self.bike_type}: {self.capacity}"
