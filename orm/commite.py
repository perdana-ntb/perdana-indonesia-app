from django.db import models
from .models import member, region, club as club_models


class RegionalCommiteMember(member.BaseCommiteMember):
    regional = models.ForeignKey(region.Region, on_delete=models.SET_NULL, null=True, blank=True)


class PengprovCommiteMember(member.BaseCommiteMember):
    province = models.ForeignKey(region.Province, on_delete=models.SET_NULL, null=True, blank=True)


class PengcabCommiteMember(member.BaseCommiteMember):
    branch = models.ForeignKey(club_models.Branch, on_delete=models.SET_NULL, null=True, blank=True)


class ClubUnitCommiteMember(member.BaseCommiteMember):
    pass
