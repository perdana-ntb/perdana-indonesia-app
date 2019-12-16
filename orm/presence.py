from django.db import models
from django_extensions.db.models import TimeStampedModel
from .member import ArcherMember
from .club import ArcheryRange

PRESENCE_STATUS_CHOICES = (
    ('0', 'Tidak Hadir'),
    ('1', 'Hadir'),
    ('2', 'Izin'),
)


class Presence(TimeStampedModel):
    member = models.ForeignKey(ArcherMember, on_delete=models.SET_NULL, related_name="member_precenses", null=True)
    supervisor = models.ForeignKey(ArcherMember, on_delete=models.SET_NULL, related_name="supervisor_precenses", null=True)
    archery_range = models.ForeignKey(ArcheryRange, on_delete=models.SET_NULL, related_name="archery_range_precenses", null=True)
    note = models.TextField(null=True, blank=True)

    # Absense is default value of presence status
    status = models.CharField(max_length=50, choices=PRESENCE_STATUS_CHOICES, default=PRESENCE_STATUS_CHOICES[0][0])

    def __str__(self):
        return self.created
