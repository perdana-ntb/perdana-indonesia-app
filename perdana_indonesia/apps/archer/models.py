from core.choices import (BLOOD_TYPE_CHOICES, GENDER_CHOICES,
                          PERDANA_USER_ROLE_CHOICES, RELIGION_CHOICES)
from core.models import TimeStampedModel
from core.utils.generator import generate_qrcode_from_text
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Archer(TimeStampedModel):
    user = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    identity_card_number = models.CharField(max_length=45, null=True, blank=True, unique=True)
    full_name = models.CharField(max_length=100, null=True, blank=True, default=None)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    born_place = models.CharField(max_length=45, null=True, blank=True)
    born_date = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    club = models.ForeignKey('club.Club', on_delete=models.SET_NULL, null=True, blank=True)
    date_register = models.DateField(null=True, blank=True)
    religion = models.CharField(
        max_length=45, choices=RELIGION_CHOICES,
        default=RELIGION_CHOICES[0][0], null=True, blank=True
    )
    blood_type = models.CharField(max_length=45, choices=BLOOD_TYPE_CHOICES, null=True, blank=True)
    disease_history = models.TextField(default=None, null=True, blank=True)

    qrcode = models.ImageField(upload_to='qr_code/%Y/%m/%d', null=True, blank=True)

    # Body section
    body_weight = models.CharField(max_length=25, null=True, blank=True, default="0")
    body_height = models.CharField(max_length=25, null=True, blank=True, default="0")
    draw_length = models.CharField(max_length=25, null=True, blank=True, default="0")
    role = models.CharField(
        max_length=100, choices=PERDANA_USER_ROLE_CHOICES, default=PERDANA_USER_ROLE_CHOICES[4][0]
    )

    is_active = models.BooleanField(default=True, null=True, blank=True)
    kelurahan = models.ForeignKey(
        'region.Kelurahan', on_delete=models.SET_NULL, null=True, blank=True
    )
    region_code_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return self.full_name or '-'

    def save(self, *args, **kwargs):
        if self.kelurahan:
            self.region_code_name = self.kelurahan.kecamatan.kabupaten.provinsi.code_name
        return super().save(*args, **kwargs)

    @property
    def isProfileComplete(self):
        return bool(
            self.user and self.full_name and self.phone and self.gender and self.born_place and
            self.born_date and self.address and self.club and self.identity_card_number and
            self.identity_card_photo and self.photo and self.public_photo and self.skck and
            self.body_weight and self.body_height and self.blood_type
        )


class ArcherApprovalStatus(TimeStampedModel):
    archer = models.OneToOneField(
        Archer, on_delete=models.SET_NULL, null=True, related_name='approval_status'
    )
    puslat_approved = models.BooleanField(default=False, null=True, blank=True)
    puslat_approved_on = models.DateTimeField(null=True, blank=True)
    puslat_approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='puslat_approval', null=True, blank=True
    )
    dpc_approved = models.BooleanField(default=False, null=True, blank=True)
    dpc_approved_on = models.DateTimeField(null=True, blank=True)
    dpc_approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='dpc_approval', null=True, blank=True
    )
    dpd_approved = models.BooleanField(default=False, null=True, blank=True)
    dpd_approved_on = models.DateTimeField(null=True, blank=True)
    dpd_approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='dpd_approval', null=True, blank=True
    )

    verified = models.BooleanField(default=False)

    def isCompletelyApproved(self) -> bool:
        return bool(
            self.puslat_approved and self.dpc_approved and self.dpd_approved
        )

    def __str__(self) -> str:
        return 'Approval status of %s' % str(self.archer)

    def save(self, **kwargs):
        self.verified = self.isCompletelyApproved()
        return super().save(**kwargs)

    class Meta:
        ordering = ['-created', '-modified']


class ArcherApprovalDocument(TimeStampedModel):
    archer = models.OneToOneField(
        Archer, on_delete=models.SET_NULL, null=True, related_name='approval_document'
    )
    # Photo will be stored as encrypted base64
    photo = models.TextField(null=True, blank=True)

    public_photo = models.ImageField(upload_to='public_photo/%Y/%m/%d', null=True, blank=True)
    identity_card_photo = models.ImageField(upload_to='id_card/%Y/%m/%d', null=True, blank=True)
    qrcode = models.ImageField(upload_to='qr_code/%Y/%m/%d', null=True, blank=True)
    skck = models.ImageField(upload_to='skck/%Y/%m/%d', null=True, blank=True)

    def __str__(self) -> str:
        return 'Approval documents of %s' % str(self.archer)

    @property
    def isDocumentComplete(self):
        return bool(
            self.photo and self.public_photo and
            self.identity_card_photo and self.skck
        )

    class Meta:
        ordering = ['-created', '-modified']


@receiver(post_save, sender=Archer)
def createArcherApprovalStatusAndDocument(sender, instance, created, **kwargs):
    ArcherApprovalStatus.objects.get_or_create(archer=instance)
    document, _ = ArcherApprovalDocument.objects.get_or_create(archer=instance)
    document.qrcode = generate_qrcode_from_text(instance.user.username)
    document.save()
