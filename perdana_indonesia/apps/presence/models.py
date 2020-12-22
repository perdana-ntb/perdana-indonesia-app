from core.choices import PRESENCE_STATUS_CHOICES
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_extensions.db.models import TimeStampedModel


class PresenceContainer(TimeStampedModel):
    title = models.CharField(max_length=255)
    creator = models.ForeignKey(
        'archer.Archer', on_delete=models.SET_NULL, null=True, blank=True
    )
    club = models.ForeignKey(
        'club.Club', on_delete=models.SET_NULL, null=True, blank=True
    )
    latitude = models.CharField(max_length=25, null=True, blank=True)
    longitude = models.CharField(max_length=25, null=True, blank=True)
    closed = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.creator:
            self.club = self.creator.club
        return super().save(*args, **kwargs)


class PresenceItem(TimeStampedModel):
    container = models.ForeignKey(
        PresenceContainer, null=True, blank=True, on_delete=models.SET_NULL
    )
    archer = models.ForeignKey(
        'archer.Archer', on_delete=models.SET_NULL, null=True, related_name='archer_presence_items'
    )
    supervisor = models.ForeignKey(
        'archer.Archer', on_delete=models.SET_NULL, null=True,
        related_name='supervisor_presence_items'
    )
    note = models.TextField(null=True, blank=True)

    # Absense is default value of presence status
    status = models.CharField(
        max_length=50, choices=PRESENCE_STATUS_CHOICES, default=PRESENCE_STATUS_CHOICES[0][0]
    )

    def __str__(self):
        return self.created


@receiver(post_save, sender=PresenceContainer)
def create_presence_items(sender, instance, created, **kwargs):
    if created:
        from archer.models import Archer
        for archer in Archer.objects.filter(club=instance.club, approved=True):
            PresenceItem.objects.create(container=instance, archer=archer)
