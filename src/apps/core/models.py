from django.db import models
from django_extensions.db.models import TimeStampedModel

# Create your models here.


class DescriptableModel(TimeStampedModel):
    name = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True
