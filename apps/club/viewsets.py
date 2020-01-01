from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.club import serializers
from core import permissions
from core.exceptions import PerdanaError
from core.pagination import CustomPageNumberPagination
from orm.models import club as club_models


class ClubViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsGeneralUser]
    serializer_class = serializers.ClubSerializer
    queryset = club_models.Club.objects.all()
    pagination_class = CustomPageNumberPagination

    def get_queryset(self, **kwargs):
        user = self.request.user
        if user.groups.filter(name=PERDANA_USER_ROLE[0]).count() > 0:
            member = user.member.regionalcommitemember
            return super().get_queryset().filter(branch__province__regional=member.regional)
        elif user.groups.filter(name=PERDANA_USER_ROLE[1]).count() > 0:
            member = user.member.pengprovcommitemember
            return super().get_queryset().filter(club__branch__province=member.province)
        elif user.groups.filter(name=PERDANA_USER_ROLE[2]).count() > 0:
            member = user.member.pengcabcommitemember
            return super().get_queryset().filter(club__branch=member.branch)
        elif user.groups.filter(name=PERDANA_USER_ROLE[3]).count() > 0:
            member = user.member.clubunitcommitemember
            if member.club:
                return super().get_queryset().filter(pk=member.club.pk)
            raise PerdanaError(message="User belum memiliki klub")
        else:
            member = user.member.archermember
            if member.club:
                return super().get_queryset().filter(pk=member.club.pk)
            raise PerdanaError(message="User belum memiliki klub")


class UnitViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsGeneralUser]
    serializer_class = serializers.UnitSerializer
    queryset = club_models.Unit.objects.all()
    pagination_class = CustomPageNumberPagination

    def get_queryset(self, **kwargs):
        user = self.request.user
        if user.groups.filter(name=PERDANA_USER_ROLE[0]).count() > 0:
            member = user.member.regionalcommitemember
            return super().get_queryset().filter(branch__province__regional=member.regional)
        elif user.groups.filter(name=PERDANA_USER_ROLE[1]).count() > 0:
            member = user.member.pengprovcommitemember
            return super().get_queryset().filter(club__branch__province=member.province)
        elif user.groups.filter(name=PERDANA_USER_ROLE[2]).count() > 0:
            member = user.member.pengcabcommitemember
            return super().get_queryset().filter(club__branch=member.branch)
        elif user.groups.filter(name=PERDANA_USER_ROLE[3]).count() > 0:
            member = user.member.clubunitcommitemember
            if member.satuan:
                return super().get_queryset().filter(pk=member.satuan.pk)
            raise PerdanaError(message="User belum memiliki satuan")
        else:
            member = user.member.archermember
            if member.satuan:
                return super().get_queryset().filter(pk=member.satuan.pk)
            raise PerdanaError(message="User belum memiliki satuan")
