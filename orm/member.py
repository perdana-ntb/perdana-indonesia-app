from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel

from . import club as club_models


class Member(TimeStampedModel):
    GENDER_CHOICES = (('pria', 'Pria'), ('wanita', 'Wanita'))

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member')
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    born_place = models.CharField(max_length=45, null=True, blank=True)
    born_date = models.DateField(null=True, blank=True)
    address = models.TextField()
    body_height = models.CharField(max_length=25, null=True, blank=True, default="0")
    body_weight = models.CharField(max_length=25, null=True, blank=True, default="0")
    draw_length = models.CharField(max_length=25, null=True, blank=True, default="0")
    club = models.ForeignKey(club_models.Club, on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    date_register = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='photo/%Y/%m/%d', null=True, blank=True)

    def __str__(self):
        return self.user.username


class Periode(models.Model):
    time_periode = models.CharField(max_length=25)

    def __str__(self):
        return self.time_periode


class Commite(TimeStampedModel):
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='commites')
    periode = models.ForeignKey(Periode, on_delete=models.SET_NULL, null=True, blank=True, related_name='commites')
    position = models.CharField(max_length=100)
    sk_number = models.CharField(max_length=100)
    sk_document = models.FileField(upload_to='docs/sk/%Y/%m/%d', null=True, blank=True)

    def __str__(self):
        return '%s => %s' % (self.position, self.member.user.username)
