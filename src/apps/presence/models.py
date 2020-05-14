from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_extensions.db.models import TimeStampedModel

from club.models import ClubUnit
from member.models import BaseMember

PRESENCE_STATUS_CHOICES = (
    ('0', 'Tidak Hadir'),
    ('1', 'Hadir'),
    ('2', 'Izin'),
)


class PresenceContainer(TimeStampedModel):
    title = models.CharField(max_length=255)
    creator = models.ForeignKey(BaseMember, on_delete=models.SET_NULL,
                                related_name="creator_presence_containers", null=True, blank=True)
    clubunit = models.ForeignKey(ClubUnit, on_delete=models.SET_NULL,
                                 related_name="presence_containers", null=True, blank=True)
    latitude = models.CharField(max_length=25, null=True, blank=True)
    longitude = models.CharField(max_length=25, null=True, blank=True)
    closed = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        basemember = self.creator.get_active_profile()
        if basemember.club:
            self.club = basemember.club
        elif basemember.satuan:
            self.satuan = basemember.satuan

        return super().save(*args, **kwargs)


class PresenceItem(TimeStampedModel):
    container = models.ForeignKey(PresenceContainer, related_name='presence_items',
                                  null=True, blank=True, on_delete=models.SET_NULL)
    member = models.ForeignKey(BaseMember, on_delete=models.SET_NULL,
                               related_name="member_presence", null=True)
    supervisor = models.ForeignKey(BaseMember, on_delete=models.SET_NULL,
                                   related_name="supervisor_presence", null=True)
    note = models.TextField(null=True, blank=True)

    # Absense is default value of presence status
    status = models.CharField(max_length=50, choices=PRESENCE_STATUS_CHOICES,
                              default=PRESENCE_STATUS_CHOICES[0][0])

    def __str__(self):
        return self.created


@receiver(post_save, sender=PresenceContainer)
def create_presence_items(sender, instance, created, **kwargs):
    if created:
        for member in BaseMember.objects.filter(clubunit=instance.clubunit,
                                                archermember__approved=True):
            PresenceItem.objects.create(container=instance, member=member)
