from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel

from . import region as region_models


class Branch(TimeStampedModel):
    name = models.CharField(max_length=100)
    address = models.TextField()
    region = models.ForeignKey(region_models.Region, on_delete=models.SET_NULL, null=True, blank=True, related_name='branchs')

    def __str__(self):
        return self.name


class Club(TimeStampedModel):
    name = models.CharField(max_length=100)
    address = models.TextField()
    date_register = models.DateField()
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='clubs')
    logo = models.ImageField(upload_to='logo/club/%Y/%m/%d', null=True, blank=True)

    def __str__(self):
        return self.name


class Unit(TimeStampedModel):
    """Unit adalah satuan seperti sekolah dan setingkat"""
    name = models.CharField(max_length=100)
    address = models.TextField()
    date_register = models.DateField()
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='units')
    logo = models.ImageField(upload_to='logo/unit/%Y/%m/%d', null=True, blank=True)
