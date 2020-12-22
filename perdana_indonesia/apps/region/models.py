from django.db import models
from django_extensions.db.models import TimeStampedModel


class Regional(TimeStampedModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['created']


class Provinsi(TimeStampedModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=100, null=True, blank=True)
    code_name = models.CharField(max_length=100, null=True, blank=True)
    regional = models.ForeignKey(Regional, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        ordering = ['created']


class Kabupaten(TimeStampedModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=100, null=True, blank=True)
    provinsi = models.ForeignKey(Provinsi, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        ordering = ['created']


class Kecamatan(TimeStampedModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=100, null=True, blank=True)
    kabupaten = models.ForeignKey(Kabupaten, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        ordering = ['created']


class Kelurahan(TimeStampedModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=100, null=True, blank=True)
    kecamatan = models.ForeignKey(Kecamatan, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        ordering = ['created']
