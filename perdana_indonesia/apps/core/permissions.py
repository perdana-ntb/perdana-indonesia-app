from rest_framework.permissions import IsAdminUser, IsAuthenticated

from core.choices import PERDANA_USER_ROLE_CHOICES

PERDANA_USER_ROLE = [x[0] for x in PERDANA_USER_ROLE_CHOICES]

PERDANA_ARCHER_USER_ROLE = PERDANA_USER_ROLE[4:]
PERDANA_CLUB_MANAGEMENT_USER_ROLE = PERDANA_USER_ROLE[3:4]
PERDANA_MANAGEMENT_USER_ROLE = PERDANA_USER_ROLE[:4]


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
        return request.user.groups.filter(name=PERDANA_USER_ROLE[3]).count() > 0


class IsMemberUser(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user.groups.filter(name=PERDANA_USER_ROLE[4]).count() > 0


class IsGeneralUser(IsAuthenticated):
    def has_permission(self, request, view):
        return bool(
            request.user.groups.filter(name__in=PERDANA_USER_ROLE).count() > 0 and
            hasattr(request.user, 'archer') and request.user.archer
        )
