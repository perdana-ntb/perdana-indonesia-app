from django.contrib.auth.models import AbstractUser
from django.db import models
from django_extensions.db.models import TimeStampedModel

# Create your models here.
CHANGE_STATUS_CHOICES = (
    ('1', 'Menunggu Persetujuan'),
    ('2', 'Diterima'),
    ('3', 'Ditolak'),
)


class PerdanaUser(AbstractUser):
    def get_active_profile(self):
        if self.members.count() > 1:
            return self.members.filter(status=CHANGE_STATUS_CHOICES[1][0],
                                       closed=True).order_by('-pk').first()
        return self.members.first()


class DescriptableModel(TimeStampedModel):
    name = models.CharField(max_length=150)
    description = models.TextField()

    class Meta:
        abstract = True
