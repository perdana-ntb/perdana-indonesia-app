from rest_framework import viewsets

from club import serializers
from club.models import ClubUnit
from member.utils import get_member_from_basemember
from core.pagination import CustomPageNumberPagination
from core.permissions import PERDANA_USER_ROLE, IsGeneralUser


class ClubUnitViewSet(viewsets.ModelViewSet):
    permission_classes = [IsGeneralUser]
    serializer_class = serializers.ClubUnitSerializer
    queryset = ClubUnit.objects.all()
    pagination_class = CustomPageNumberPagination

    def get_queryset(self, **kwargs):
        user = self.request.user
        member = get_member_from_basemember(user.basemember)

        if user.groups.filter(name=PERDANA_USER_ROLE[0]).count() > 0:
            return super().get_queryset().filter(branch__province__regional=member.regional)
        elif user.groups.filter(name=PERDANA_USER_ROLE[1]).count() > 0:
            return super().get_queryset().filter(branch__province=member.province)
        elif user.groups.filter(name=PERDANA_USER_ROLE[2]).count() > 0:
            return super().get_queryset().filter(branch=member.branch)
        elif user.groups.filter(name=PERDANA_USER_ROLE[3]).count() > 0:
            return super().get_queryset().filter(pk=member.clubunit.pk)
        else:
            return []
