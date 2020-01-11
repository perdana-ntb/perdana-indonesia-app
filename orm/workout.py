from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel
from core.models import DescriptableModel
from . import member as member_models


class WorkOutItem(DescriptableModel):
    unit = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class WorkOutTarget(TimeStampedModel):
    item = models.ForeignKey(WorkOutItem, related_name='wo_targets', on_delete=models.SET_NULL, null=True)
    member = models.ForeignKey(member_models.BaseMember, related_name='wo_targets', on_delete=models.SET_NULL, null=True)
    target = models.IntegerField(default=0)
    unit = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.item.name


class WorkOut(TimeStampedModel):
    item = models.ForeignKey(WorkOutItem, related_name='workouts', on_delete=models.SET_NULL, null=True)
    member = models.ForeignKey(member_models.BaseMember, related_name='workouts', on_delete=models.SET_NULL, null=True)
    target = models.ForeignKey(WorkOutTarget, related_name='workouts', on_delete=models.SET_NULL, null=True)
    achievement = models.CharField(max_length=100)

    def __str__(self):
        return self.item.name


class WorkOutContainer(TimeStampedModel):
    workouts = models.ManyToManyField(WorkOut, related_name='wo_containers')
    finished = models.BooleanField(default=False)

    def __str__(self):
        return '%s -> %s' % (self.pk, self.finished)
