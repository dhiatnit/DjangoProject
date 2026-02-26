from django.db import models

class Rides(models.Model):
    rideId = models.AutoField(primary_key=True)

    user = models.ForeignKey(
        "Users",
        on_delete=models.CASCADE
    )

    bike = models.ForeignKey(
        "Bikes",
        on_delete=models.CASCADE
    )

    startStation = models.ForeignKey(
        "Stations",
        on_delete=models.CASCADE,
        related_name="ride_start_station"
    )

    endStation = models.ForeignKey(
        "Stations",
        on_delete=models.CASCADE,
        related_name="ride_end_station"
    )

    startTime = models.DateTimeField()
    endTime = models.DateTimeField()

    distance = models.FloatField()

    batteryLevelStart = models.IntegerField()
    batteryLevelEnd = models.IntegerField()

    def __str__(self):
        return f"Ride {self.rideId}"