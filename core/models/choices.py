from django.db import models


class BikeType(models.TextChoices):
    ELECTRIC = "electric", "Electric"
    NON_ELECTRIC = "non_electric", "Non Electric"


class BikeStatus(models.TextChoices):
    AVAILABLE = "available", "Available"
    NOT_AVAILABLE = "not_available", "Not Available"
