from core.choices import BLOOD_TYPE_CHOICES, GENDER_CHOICES, RELIGION_CHOICES
from core.models import TimeStampedModel
from django.contrib.auth.models import User
from django.db import models


class Archer(TimeStampedModel):
    user = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    full_name = models.CharField(max_length=100, null=True, blank=True, default=None)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    born_place = models.CharField(max_length=45, null=True, blank=True)
    born_date = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    club = models.ForeignKey(
        'club.Club', on_delete=models.SET_NULL, null=True, blank=True
    )
    date_register = models.DateField(null=True, blank=True)
    religion = models.CharField(
        max_length=45, choices=RELIGION_CHOICES,
        default=RELIGION_CHOICES[0][0], null=True, blank=True
    )

    blood_type = models.CharField(max_length=45, choices=BLOOD_TYPE_CHOICES, null=True, blank=True)
    disease_history = models.TextField(default=None, null=True, blank=True)

    identity_card_number = models.CharField(max_length=45, null=True, blank=True, unique=True)
    identity_card_photo = models.ImageField(upload_to='id_card/%Y/%m/%d', null=True, blank=True)
    photo = models.ImageField(upload_to='photo/%Y/%m/%d', null=True, blank=True)
    public_photo = models.ImageField(upload_to='public_photo/%Y/%m/%d', null=True, blank=True)
    qrcode = models.ImageField(upload_to='qr_code/%Y/%m/%d', null=True, blank=True)
    skck = models.ImageField(upload_to='skck/%Y/%m/%d', null=True, blank=True)

    # Body section
    body_weight = models.CharField(max_length=25, null=True, blank=True, default="0")
    body_height = models.CharField(max_length=25, null=True, blank=True, default="0")
    draw_length = models.CharField(max_length=25, null=True, blank=True, default="0")

    # Approval section
    verified = models.BooleanField(default=False, null=True, blank=True)
    approved = models.BooleanField(default=False, null=True, blank=True)
    approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='archers_approval', null=True, blank=True
    )
    kelurahan = models.ForeignKey(
        'region.Kelurahan', on_delete=models.SET_NULL,  null=True, blank=True
    )
    region_code_name = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.kelurahan:
            self.region_code_name = self.kelurahan.kecamatan.kabupaten.provinsi.code_name
        return super().save(*args, **kwargs)

    @property
    def isProfileComplete(self):
        return bool(
            self.user and self.full_name and self.phone and self.gender and self.born_place
            and self.born_date and self.address and self.club and self.identity_card_number
            and self.identity_card_photo and self.photo and self.public_photo and self.skck
            and self.body_weight and self.body_height and self.blood_type
        )

    def getUserGroup(self):
        return self.user.groups.first()
