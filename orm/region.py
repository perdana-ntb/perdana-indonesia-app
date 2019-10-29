from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel


class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
