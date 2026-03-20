from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models




class Station(models.Model):
    station_id = models.AutoField(primary_key=True)
    zone = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)])
    address = models.CharField(max_length=255)

    class Meta:
        indexes = [models.Index(fields=["zone"])]

    def __str__(self):
        return f"Station {self.station_id} - Zone {self.zone}"


class StationCapacity(models.Model):
    station = models.ForeignKey("core.station", on_delete=models.CASCADE)
    bike_type = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["station", "bike_type"], name="unique_station_bike_type")
        ]

    def __str__(self):
        return f"{self.station} - {self.bike_type}: {self.capacity}"
