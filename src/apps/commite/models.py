from django.db import models

from club.models import Branch
from member.models import BaseMember
from region.models import Province, Region


class Periode(models.Model):
    start_periode = models.CharField(max_length=25)
    end_periode = models.CharField(max_length=25)

    def __str__(self):
        return '%s/%s' % (self.start_periode, self.end_periode)


class CommitePosition(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name


class BaseCommiteMember(BaseMember):
    periode = models.ForeignKey('Periode', on_delete=models.SET_NULL, null=True, blank=True)
    position = models.ForeignKey(CommitePosition, on_delete=models.SET_NULL, null=True, blank=True)
    sk_number = models.CharField(max_length=100, null=True, blank=True)
    sk_document = models.FileField(upload_to='docs/sk/%Y/%m/%d', null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return '%s => %s' % (self.position, self.user.username)


class RegionalCommiteMember(BaseCommiteMember):
    regional = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)


class PengprovCommiteMember(BaseCommiteMember):
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True, blank=True)


class PengcabCommiteMember(BaseCommiteMember):
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)


class ClubUnitCommiteMember(BaseCommiteMember):
    pass
