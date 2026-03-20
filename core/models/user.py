from django.db import models
from django.db.models import Q


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

    def __str__(self):
        return f"user {self.user_id}"

    class Meta:
        indexes = [
            models.Index(fields=['surname']),
            models.Index(fields=['name', 'surname']),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=['email'],
                name='unique_user_email'
            ),
            models.CheckConstraint(
                condition=~Q(name=''),
                name='name_not_empty'
            ),
            models.CheckConstraint(
                condition=~Q(surname=''),
                name='surname_not_empty'
            ),
        ]