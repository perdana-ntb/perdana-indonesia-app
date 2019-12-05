from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel

from core.models import DescriptableModel

from . import member as member_models


class Bow(DescriptableModel):
    owner = models.ForeignKey(member_models.ArcherMember, on_delete=models.CASCADE, related_name='bows')

    def __str__(self):
        return self.name


class Arrow(DescriptableModel):
    owner = models.ForeignKey(member_models.ArcherMember, on_delete=models.CASCADE, related_name='arrows')

    def __str__(self):
        return self.name
