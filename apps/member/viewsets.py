# Create your views here.
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.member import serializers
from core import permissions as core_perm
from core.exceptions import PerdanaError
from core.permissions import PERDANA_USER_ROLE
from core.utils.generator import generate_qrcode_from_text
from core.utils.permission_checker import get_user_group
from orm.models import member as member_models


class LoginViewset(views.APIView):
    permission_classes = []
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = authenticate(**serializer.validated_data)
            if user:
                if hasattr(user, 'member'):
                    if hasattr(user.member, 'archermember'):
                        if not user.member.archermember.approved:
                            raise PerdanaError(message="User sedang dalam proses review oleh admin", status_code=status.HTTP_403_FORBIDDEN)

                    group = get_user_group(user)
                    return Response({
                        'token': user.auth_token.key,
                        'role': group if group else None,
                        'member': serializers.BaseArcherMemberSerializer(user.member).to_representation(user.member)
                    })
                raise PerdanaError(message="Jenis user tidak dapat melakukan aksi ini", status_code=status.HTTP_403_FORBIDDEN)
            raise PerdanaError(message="Username dan atau password salah", status_code=status.HTTP_400_BAD_REQUEST)
        return Response(**serializer.validated_data, status=status.HTTP_400_BAD_REQUEST)


class RegisterViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = []
    serializer_class = serializers.ArcherMemberSerializer


class ArcherMemberViewset(viewsets.ReadOnlyModelViewSet):
    permission_classes = [core_perm.IsGeneralUser]
    serializer_class = serializers.ArcherMemberSerializer
    queryset = member_models.ArcherMember.objects.filter(approved=True)

    def get_queryset(self, **kwargs):
        user = self.request.user
        if user.groups.filter(name=PERDANA_USER_ROLE[0]).count() > 0:
            member = user.member.regionalcommitemember
            return super().get_queryset().filter(
                Q(club__branch__province__regional=member.regional) |
                Q(satuan__branch__province__regional=member.regional))
        elif user.groups.filter(name=PERDANA_USER_ROLE[1]).count() > 0:
            member = user.member.pengprovcommitemember
            return super().get_queryset().filter(
                Q(club__branch__province=member.province) |
                Q(satuan__branch__province=member.province))
        elif user.groups.filter(name=PERDANA_USER_ROLE[2]).count() > 0:
            member = user.member.pengcabcommitemember
            return super().get_queryset().filter(
                Q(club__branch=member.branch) |
                Q(satuan__branch=member.branch))
        elif user.groups.filter(name=PERDANA_USER_ROLE[3]).count() > 0:
            member = user.member.clubunitcommitemember
            if member.club:
                return super().get_queryset().filter(club=member.club)
            elif member.satuan:
                return super().get_queryset().filter(satuan=member.satuan)
        else:
            return super().get_queryset().filter(pk=user.member.archermember.pk)

    @action(detail=True, methods=['get'], permission_classes=[core_perm.IsClubOrSatuanManagerUser])
    def approve(self, request, pk=None):
        obj = get_object_or_404(member_models.ArcherMember, pk=self.kwargs.get('pk'))
        obj.approved = True
        obj.approved_by = self.request.user
        obj.save()
        return Response(self.serializer_class(obj).data)

    @action(detail=False, methods=['get'], permission_classes=[core_perm.IsClubOrSatuanManagerUser])
    def applicants(self, request):
        try:
            member = self.request.user.member.clubunitcommitemember
            qs = member_models.ArcherMember.objects.filter(approved=False)
            if member.club:
                qs = qs.filter(club=member.club)
            elif member.satuan:
                qs = qs.filter(satuan=member.satuan)

            return Response(self.serializer_class(qs, many=True).data)
        except AttributeError:
            raise PerdanaError(message='User belum memiliki klub atau satuan')
