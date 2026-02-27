from django.db import models


class Station(models.Model):
    stationId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
