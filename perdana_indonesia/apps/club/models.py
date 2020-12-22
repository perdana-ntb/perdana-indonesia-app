from core.choices import CLUB_UNIT_TYPE_CHOICES
from core.models import TimeStampedModel
from django.db import models


class Club(TimeStampedModel):
    name = models.CharField(max_length=100)
    central = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='branchs'
    )
    address = models.TextField()
    kelurahan = models.ForeignKey(
        'region.Kelurahan', on_delete=models.SET_NULL, null=True, blank=True
    )
    org_type = models.CharField(
        max_length=20, choices=CLUB_UNIT_TYPE_CHOICES, default=CLUB_UNIT_TYPE_CHOICES[0][0]
    )
    logo = models.ImageField(upload_to='logo/%Y/%m/%d', null=True, blank=True)
    date_register = models.DateField()

    def __str__(self):
        return self.name


class ArcheryRange (TimeStampedModel):
    name = models.CharField(max_length=255)
    address = models.TextField(null=True)
    kelurahan = models.ForeignKey(
        'region.Kelurahan', on_delete=models.SET_NULL, null=True, blank=True
    )
    latitude = models.CharField(max_length=25)
    longitude = models.CharField(max_length=25)
    managed_by = models.ForeignKey(
        Club, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.name
