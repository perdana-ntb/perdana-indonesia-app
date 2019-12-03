from django.contrib.auth.models import Group
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.

PERDANA_USER_ROLE = [
    'regional',
    'pengprov',
    'pengcab',
    'club-manager',
    'satuan-manager'
]


class IsRegionalUser(IsAdminUser):
    def has_permission(self, request, view):
        return request.user.groups.filter(name=PERDANA_USER_ROLE[0]).count() > 0


class IsPengprovUser(IsAdminUser):
    def has_permission(self, request, view):
        return request.user.groups.filter(name=PERDANA_USER_ROLE[1]).count() > 0


class IsPengcabUser(IsAdminUser):
    def has_permission(self, request, view):
        return request.user.groups.filter(name=PERDANA_USER_ROLE[2]).count() > 0


class IsClubOrSatuanManagerUser(IsAdminUser):
    def has_permission(self, request, view):
        return request.user.groups.filter(name=PERDANA_USER_ROLE[2]).count() > 0


class IsMemberUser(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user.groups.filter(name=PERDANA_USER_ROLE[3]).count() > 0


class IsGeneralUser(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user.groups.filter(name__in=PERDANA_USER_ROLE).count() > 0
