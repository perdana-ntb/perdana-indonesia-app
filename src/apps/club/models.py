from django.db import models
from django_extensions.db.models import TimeStampedModel

from region.models import Province
from core.models import DescriptableModel


class Bow(DescriptableModel):
    owner = models.ForeignKey('member.BaseMember', on_delete=models.CASCADE, related_name='bows')

    def __str__(self):
        return self.name


class Arrow(DescriptableModel):
    owner = models.ForeignKey('member.BaseMember', on_delete=models.CASCADE, related_name='arrows')

    def __str__(self):
        return self.name


class Branch(TimeStampedModel):
    name = models.CharField(max_length=100)
    address = models.TextField()
    province = models.ForeignKey(Province, on_delete=models.SET_NULL,
                                 null=True, blank=True, related_name='branchs')

    def __str__(self):
        return self.name


class ClubUnit(TimeStampedModel):
    CLUB_UNIT_TYPE_CHOICES = (
        ('club', 'Club'),
        ('unit', 'Unit')
    )
    name = models.CharField(max_length=100)
    address = models.TextField()
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL,
                               null=True, blank=True, related_name='clubunits')
    date_register = models.DateField()
    logo = models.ImageField(upload_to='logo/%Y/%m/%d', null=True, blank=True)
    type = models.CharField(max_length=20, choices=CLUB_UNIT_TYPE_CHOICES,
                            default=CLUB_UNIT_TYPE_CHOICES[0][0])

    def __str__(self):
        return self.name


class ArcheryRange (models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(null=True)
    latitude = models.CharField(max_length=25)
    longitude = models.CharField(max_length=25)
    managed_by = models.ForeignKey(ClubUnit, on_delete=models.SET_NULL,
                                   related_name='archery_ranges', null=True, blank=True)

    def __str__(self):
        return self.name
