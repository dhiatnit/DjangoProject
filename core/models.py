from django.db import models
from django.db.models import Q
from django.core.validators import MinValueValidator, MaxValueValidator

class BikeType(models.TextChoices):
    ELECTRIC = "electric", "Electric"
    NON_ELECTRIC = "non_electric", "Non Electric"

class Stations(models.Model):

    station_id = models.AutoField(primary_key=True)

    zone = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)]
    )

    address = models.CharField(max_length=255)

    class Meta:
        indexes = [
            models.Index(fields=["zone"]),
        ]

    def __str__(self):
        return f"Station {self.station_id} - Zone {self.zone}"

class StationCapacity(models.Model):

    station = models.ForeignKey(
        Stations,
        on_delete=models.CASCADE,
        related_name="capacities"
    )

    bike_type = models.CharField(
        max_length=20,
        choices=BikeType.choices
    )

    capacity = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['station', 'bike_type'],
                name='unique_station_biketype'
            )
        ]

    def __str__(self):
        return f"{self.station} - {self.bike_type}"

class Bikes(models.Model):

    class BikeStatusChoices(models.TextChoices):
        AVAILABLE = "available", "Available"
        NOT_AVAILABLE = "not_available", "Not Available"

    bike_id = models.AutoField(primary_key=True)

    station = models.ForeignKey(
        Stations,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bikes"
    )

    bike_type = models.CharField(
        max_length=20,
        choices=BikeType.choices
    )

    battery_level = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True
    )

    bike_status = models.CharField(
        max_length=20,
        choices=BikeStatusChoices.choices,
        default=BikeStatusChoices.AVAILABLE
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                        Q(bike_type="electric", battery_level__isnull=False) |
                        Q(bike_type="non_electric", battery_level__isnull=True)
                ),
                name="battery_consistency_for_each_type"
            ),

            models.CheckConstraint(
                check=(
                        Q(bike_status="available", station__isnull=False) |
                        Q(bike_status="not_available", station__isnull=True)
                ),
                name="bike_station_consistency"
            ),


        ]
        indexes = [
            models.Index(fields=["station"]),
            models.Index(fields=["bike_status"]),
            models.Index(fields=["station", "bike_status"]),
            models.Index(fields=["station", "bike_status", "battery_level"]),
        ]



    def __str__(self):
        return f"Bike {self.bike_id}"


class Maintenance(models.Model):

    maintenance_id = models.AutoField(primary_key=True)

    bike = models.ForeignKey(
        Bikes,
        on_delete=models.CASCADE,
        related_name="maintenances"
    )

    date = models.DateField()

    cost = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    warehouse_id = models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=["bike"]),
            models.Index(fields=["bike", "date"]),
            models.Index(fields=["date", "cost"]),
        ]


    def __str__(self):
        return f"Maintenance {self.maintenance_id} - Bike {self.bike.bike_id}"
