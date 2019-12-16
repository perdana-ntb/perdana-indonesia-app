from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel

from core.models import DescriptableModel
from orm.club import ArcheryRange
from orm.member import ArcherMember

PRACTICE_STATUS_CHOICES = (
    ('0', 'Waiting'),
    ('1', 'Rejected'),
    ('3', 'Approved'),
)


class TargetType(DescriptableModel):
    def __str__(self):
        return self.name


class Practice(TimeStampedModel):
    member = models.ForeignKey(ArcherMember, on_delete=models.SET_NULL, related_name="practices", null=True)
    archery_range = models.ForeignKey(ArcheryRange, on_delete=models.SET_NULL, related_name="practices", null=True)
    target_type = models.ForeignKey(TargetType, on_delete=models.SET_NULL, related_name='practices', null=True)

    distance = models.FloatField(default=1)
    series = models.IntegerField(default=1)
    arrow = models.IntegerField(default=1)

    status = models.CharField(max_length=50, choices=PRACTICE_STATUS_CHOICES,
                              default=PRACTICE_STATUS_CHOICES[0][0], null=True, blank=True)

    signed = models.BooleanField(default=False, null=True, blank=True)
    signed_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="practices", null=True, blank=True)

    completed = models.BooleanField(default=False, null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.member.user.username


class PracticeSeries(TimeStampedModel):
    practice = models.ForeignKey(Practice, on_delete=models.CASCADE, related_name='practice_series')
    photo = models.ImageField(upload_to='practice/sk/%Y/%m/%d', null=True, blank=True)
    closed = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.practice


class PracticeScore(models.Model):
    score = models.IntegerField(default=0)
    serie = models.ForeignKey(PracticeSeries, on_delete=models.CASCADE, related_name='scores')

    def __str__(self):
        return self.score
