from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_extensions.db.models import TimeStampedModel

from core.models import DescriptableModel
from orm.club import ArcheryRange
from orm.member import ArcherMember, BaseMember

PRACTICE_STATUS_CHOICES = (
    ('0', 'Waiting'),
    ('1', 'Rejected'),
    ('3', 'Approved'),
)


class TargetType(DescriptableModel):
    def __str__(self):
        return self.name


class PracticeContainer(TimeStampedModel):
    member = models.ForeignKey(BaseMember, on_delete=models.SET_NULL, related_name="practices", null=True)
    archery_range = models.ForeignKey(ArcheryRange, on_delete=models.SET_NULL, related_name="practices", null=True)
    # target_type = models.ForeignKey(TargetType, on_delete=models.SET_NULL, related_name='practices', null=True)
    target_type = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    latitude = models.CharField(max_length=25, null=True, blank=True)
    longitude = models.CharField(max_length=25, null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    distance = models.FloatField(default=1)
    series = models.IntegerField(default=1)
    arrow = models.IntegerField(default=1)

    status = models.CharField(max_length=50, choices=PRACTICE_STATUS_CHOICES,
                              default=PRACTICE_STATUS_CHOICES[0][0], null=True, blank=True)

    signed = models.BooleanField(default=False, null=True, blank=True)
    signed_by = models.ForeignKey(BaseMember, on_delete=models.SET_NULL, related_name="signed_practices", null=True, blank=True)

    completed = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.member.user.username

    def save(self, **kwargs):
        if self.archery_range:
            self.address = self.archery_range.address
            self.latitude = self.archery_range.latitude
            self.longitude = self.archery_range.longitude
        return super().save(**kwargs)


class PracticeSeries(TimeStampedModel):
    serie = models.IntegerField(default=0)
    practice_container = models.ForeignKey(PracticeContainer, on_delete=models.CASCADE, related_name='practice_series')
    photo = models.ImageField(upload_to='practice/sk/%Y/%m/%d', null=True, blank=True)
    closed = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.practice_container.note


class PracticeScore(models.Model):
    score = models.IntegerField(default=0)
    serie = models.ForeignKey(PracticeSeries, on_delete=models.CASCADE, related_name='scores')
    filled = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % self.score
    


@receiver(post_save, sender=PracticeContainer)
def create_practice_series(sender, instance, created, **kwargs):
    if created:
        for i in range(0, instance.series):
            serie = PracticeSeries.objects.create(practice_container=instance, serie=i+1)
            for i in range(0, instance.arrow):
                PracticeScore.objects.create(serie=serie)
