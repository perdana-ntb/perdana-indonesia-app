import jsonfield
from django.db import models
from django_extensions.db.models import TimeStampedModel


class EasyLogging(TimeStampedModel):
    username = models.CharField(max_length=150)
    endpoint = models.TextField()
    method = models.CharField(max_length=25)
    ip_address = models.CharField(max_length=25, null=True, blank=True)
    request_json = jsonfield.JSONField(null=True, blank=True)
    response_json = jsonfield.JSONField(null=True, blank=True)
    kwargs = jsonfield.JSONField(null=True, blank=True)

    def __str__(self) -> str:
        return self.username
