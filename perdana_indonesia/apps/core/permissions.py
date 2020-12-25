from rest_framework.permissions import IsAdminUser, IsAuthenticated

PERDANA_USER_ROLE = [
    'regional',
    'pengprov',
    'pengcab',
    'club-satuan-manager',
    'archer'
]

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
        return request.user.groups.filter(name__in=PERDANA_USER_ROLE).count() > 0
