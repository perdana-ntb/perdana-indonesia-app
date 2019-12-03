from django.db import models
from django_extensions.db.models import TimeStampedModel
from .member import Member
from .club import ArcheryRange


class Precense(TimeStampedModel):
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="member_precenses", null=True)
    supervisor = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="supervisor_precenses", null=True)
    archery_range = models.ForeignKey(ArcheryRange, on_delete=models.SET_NULL, related_name="archery_range_precenses", null=True)
    note = models.TextField(null=True)

    def __str__(self):
        return self.created
