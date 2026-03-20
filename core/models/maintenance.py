from django.db import models


class Maintenance(models.Model):
    maintenance_id = models.AutoField(primary_key=True)
    bike = models.ForeignKey("core.bike", on_delete=models.CASCADE)
    note = models.TextField(blank=True)
    date = models.DateField()
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    repair_place = models.CharField(max_length=255)

    class Meta:
        indexes = [models.Index(fields=["bike", "date"])]

    def __str__(self):
        return f"Maintenance {self.maintenance_id} - Bike {self.bike_id}"
