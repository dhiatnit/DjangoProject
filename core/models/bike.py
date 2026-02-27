from django.db import models


class Bike(models.Model):
    bikeId = models.AutoField(primary_key=True)
    code = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"bike {self.code}"
