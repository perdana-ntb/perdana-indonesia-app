from core.models import DescriptableModel
from django.db import models
from django_extensions.db.models import TimeStampedModel


class WorkOutItem(DescriptableModel):
    unit = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class WorkOutTarget(TimeStampedModel):
    item = models.ForeignKey(
        WorkOutItem, related_name='wo_targets', on_delete=models.SET_NULL, null=True
    )
    archer = models.ForeignKey(
        'archer.Archer', related_name='wo_targets', on_delete=models.SET_NULL, null=True
    )
    target = models.IntegerField(default=0)
    unit = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.item.name


class WorkOut(TimeStampedModel):
    item = models.ForeignKey(
        WorkOutItem, related_name='workouts', on_delete=models.SET_NULL, null=True
    )
    archer = models.ForeignKey(
        'archer.Archer', related_name='workouts', on_delete=models.SET_NULL, null=True
    )
    target = models.ForeignKey(
        WorkOutTarget, related_name='workouts', on_delete=models.SET_NULL, null=True
    )
    achievement = models.CharField(max_length=100)

    def __str__(self):
        return self.item.name


class WorkOutContainer(TimeStampedModel):
    workouts = models.ManyToManyField(WorkOut, related_name='wo_containers')
    finished = models.BooleanField(default=False)

    def __str__(self):
        return '%s -> %s' % (self.pk, self.finished)
