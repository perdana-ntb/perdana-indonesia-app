# from core.choices import CLUB_UNIT_TYPE_CHOICES
from core.choices import CLUB_UNIT_TYPE_CHOICES
from core.models import TimeStampedModel
from django.db import models

from club.choices import WEEKDAY_CHOICES


class Club(TimeStampedModel):
    name = models.CharField(max_length=255)
    organisation_id = models.CharField(
        max_length=100, null=True, blank=True, unique=True
    )
    central = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='branchs'
    )
    address = models.TextField()
    org_type = models.CharField(
        max_length=20, choices=CLUB_UNIT_TYPE_CHOICES, default=CLUB_UNIT_TYPE_CHOICES[0][0]
    )
    logo = models.ImageField(upload_to='logo/%Y/%m/%d', null=True, blank=True)
    date_register = models.DateField(null=True, blank=True)

    province_code = models.CharField(max_length=100, null=True, blank=True)
    city_code = models.CharField(max_length=100, null=True, blank=True)
    district_code = models.CharField(max_length=100, null=True, blank=True)
    village = models.ForeignKey(
        'region.Kelurahan', on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.village:
            self.district_code = self.village.kecamatan.code
            self.city_code = self.village.kecamatan.kabupaten.code
            self.province_code = self.village.kecamatan.kabupaten.provinsi.code
        return super().save(*args, **kwargs)


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


class PracticeSchedule(models.Model):
    puslat = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, blank=True)
    archery_range = models.ForeignKey(
        ArcheryRange, on_delete=models.SET_NULL, null=True, blank=True
    )
    practice_day = models.CharField(max_length=5, choices=WEEKDAY_CHOICES, null=True, blank=True)
    practice_start_time = models.TimeField(null=True, blank=True)
    practice_end_time = models.TimeField(null=True, blank=True)

    def __str__(self) -> str:
        return 'Schedule of %s' % self.puslat.name

    @property
    def practice_day_name(self):
        return WEEKDAY_CHOICES[self.practice_day][1]
