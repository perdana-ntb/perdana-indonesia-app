from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel


class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Province(models.Model):
    name = models.CharField(max_length=100)
    regional = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True, related_name='provinces')

    def __str__(self):
        return self.name
