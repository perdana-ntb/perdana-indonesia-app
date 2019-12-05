from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel

from . import club as club_models


class BaseMember(TimeStampedModel):
    GENDER_CHOICES = (('pria', 'Pria'), ('wanita', 'Wanita'))

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member')
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    born_place = models.CharField(max_length=45, null=True, blank=True)
    born_date = models.DateField(null=True, blank=True)
    address = models.TextField()
    club = models.ForeignKey(club_models.Club, on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    satuan = models.ForeignKey(club_models.Unit, on_delete=models.SET_NULL, null=True, blank=True, related_name='members')

    photo = models.ImageField(upload_to='photo/%Y/%m/%d', null=True, blank=True)
    qrcode = models.ImageField(upload_to='qr_code/%Y/%m/%d', null=True, blank=True)

    def __str__(self):
        return self.user.username


class ArcherMember(BaseMember):
    body_height = models.CharField(max_length=25, null=True, blank=True, default="0")
    body_weight = models.CharField(max_length=25, null=True, blank=True, default="0")
    draw_length = models.CharField(max_length=25, null=True, blank=True, default="0")
    date_register = models.DateField(null=True, blank=True)
    approved = models.BooleanField(default=False, null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET, related_name='member_approval', null=True, blank=True)

    def __str__(self):
        return self.user.username


class CommiteMember(BaseMember):
    periode = models.ForeignKey('Periode', on_delete=models.SET_NULL, null=True, blank=True, related_name='commites')
    position = models.CharField(max_length=100)
    sk_number = models.CharField(max_length=100)
    sk_document = models.FileField(upload_to='docs/sk/%Y/%m/%d', null=True, blank=True)

    def __str__(self):
        return '%s => %s' % (self.position, self.user.username)


class Periode(models.Model):
    time_periode = models.CharField(max_length=25)

    def __str__(self):
        return self.time_periode
