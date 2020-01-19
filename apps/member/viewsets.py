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
from core.pagination import CustomPageNumberPagination
from core.permissions import PERDANA_USER_ROLE
from core.utils.generator import generate_qrcode_from_text
from core.utils.permission_checker import get_user_group
from orm.models import club as club_models
from orm.models import member as member_models
from orm.models import region as region_models


class LoginViewset(views.APIView):
    permission_classes = []
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = authenticate(**serializer.validated_data)
            if user:
                if hasattr(user, 'members'):
                    if hasattr(user.get_active_profile(), 'archermember'):
                        if not user.get_active_profile().archermember.approved:
                            raise PerdanaError(message="User sedang dalam proses review oleh admin", status_code=status.HTTP_403_FORBIDDEN)

                    group = get_user_group(user)
                    return Response({
                        'token': user.auth_token.key,
                        'role': group if group else None,
                        'member': serializers.BaseArcherMemberSerializer(user.get_active_profile()).to_representation(user.get_active_profile())
                    })
                raise PerdanaError(message="Jenis user tidak dapat melakukan aksi ini", status_code=status.HTTP_403_FORBIDDEN)
            raise PerdanaError(message="Username dan atau password salah", status_code=status.HTTP_400_BAD_REQUEST)
        return Response(**serializer.validated_data, status=status.HTTP_400_BAD_REQUEST)


class RegisterViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = []
    serializer_class = serializers.RegisterSerializer


class UserProfileViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [core_perm.IsGeneralUser]

    def list(self, request):
        member = self.request.user.get_active_profile()
        if hasattr(member, 'archermember'):
            return Response(serializers.ArcherMemberSerializer(member.archermember).data)
        elif hasattr(member, 'clubunitcommitemember'):
            return Response(serializers.ClubUnitCommiteMemberSerializer(member.clubunitcommitemember).data)
        else:
            raise PerdanaError(message="Jenis user tidak dapat melakukan aksi ini")

    @action(detail=False, methods=['post'], permission_classes=[core_perm.IsGeneralUser])
    def change(self, request, pk=None):
        member = self.request.user.get_active_profile()
        if hasattr(member, 'archermember'):
            serializer = serializers.ArcherMemberProfileUpdateSerializer(instance=member.archermember, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializers.ArcherMemberSerializer(member.archermember).data)
        elif hasattr(member, 'clubunitcommitemember'):
            serializer = serializers.ClubUnitCommiteMemberSerializer(instance=member.clubunitcommitemember, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializers.ClubUnitCommiteMemberSerializer(member.clubunitcommitemember).data)
        else:
            raise PerdanaError(message="Jenis user tidak dapat melakukan aksi ini")


class ArcherMemberViewset(viewsets.ReadOnlyModelViewSet):
    permission_classes = [core_perm.IsGeneralUser]
    serializer_class = serializers.ArcherMemberSerializer
    queryset = member_models.ArcherMember.objects.filter(approved=True)
    pagination_class = CustomPageNumberPagination

    def get_queryset(self, **kwargs):
        user = self.request.user
        if user.groups.filter(name=PERDANA_USER_ROLE[0]).count() > 0:
            member = user.get_active_profile().regionalcommitemember
            return super().get_queryset().filter(
                Q(club__branch__province__regional=member.regional) |
                Q(satuan__branch__province__regional=member.regional))
        elif user.groups.filter(name=PERDANA_USER_ROLE[1]).count() > 0:
            member = user.get_active_profile().pengprovcommitemember
            return super().get_queryset().filter(
                Q(club__branch__province=member.province) |
                Q(satuan__branch__province=member.province))
        elif user.groups.filter(name=PERDANA_USER_ROLE[2]).count() > 0:
            member = user.get_active_profile().pengcabcommitemember
            return super().get_queryset().filter(
                Q(club__branch=member.branch) |
                Q(satuan__branch=member.branch))
        elif user.groups.filter(name=PERDANA_USER_ROLE[3]).count() > 0:
            member = user.get_active_profile().clubunitcommitemember
            if member.club:
                return super().get_queryset().filter(club=member.club)
            elif member.satuan:
                return super().get_queryset().filter(satuan=member.satuan)
        else:
            return super().get_queryset().filter(pk=user.get_active_profile().archermember.pk)

    @action(detail=True, methods=['put'], permission_classes=[core_perm.IsClubOrSatuanManagerUser])
    def change(self, request, pk=None):
        instance = get_object_or_404(member_models.ArcherMember, pk=self.kwargs.get('pk'))
        serializer = self.serializer_class(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(self.serializer_class(instance).data)

    @action(detail=True, methods=['get'], permission_classes=[core_perm.IsClubOrSatuanManagerUser])
    def approve(self, request, pk=None):
        obj = get_object_or_404(member_models.ArcherMember, pk=self.kwargs.get('pk'))
        obj.approved = True
        obj.approved_by = self.request.user

        obj.qrcode = generate_qrcode_from_text(obj.user.username)
        obj.save()
        return Response(self.serializer_class(obj).data)

    @action(detail=False, methods=['get'], permission_classes=[core_perm.IsClubOrSatuanManagerUser])
    def applicants(self, request):
        try:
            member = self.request.user.get_active_profile().clubunitcommitemember
            qs = member_models.ArcherMember.objects.filter(approved=False)
            if member.club:
                qs = qs.filter(club=member.club)
            elif member.satuan:
                qs = qs.filter(satuan=member.satuan)

            return Response(self.serializer_class(qs, many=True).data)
        except AttributeError:
            raise PerdanaError(message='User belum memiliki klub atau satuan')


class ArcherMemberApplicantViewset(viewsets.ReadOnlyModelViewSet):
    permission_classes = [core_perm.IsGeneralUser]
    serializer_class = serializers.ArcherMemberSerializer
    queryset = member_models.ArcherMember.objects.filter(approved=False)

    def get_queryset(self):
        queryset = super().get_queryset()
        try:
            member = self.request.user.get_active_profile().clubunitcommitemember
            if member.club:
                qs = queryset.filter(club=member.club)
            elif member.satuan:
                qs = queryset.filter(satuan=member.satuan)
            return qs
        except AttributeError:
            raise PerdanaError(message='User belum memiliki klub atau satuan')

    @action(methods=['POST'], detail=True, serializer_class=serializers.ApproveArcherMemberSerializer)
    def approve(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = self.get_object()
        instance.user.username = serializer.validated_data.get('register_number')
        instance.user.save()

        instance.approved = True
        instance.approved_by = request.user
        instance.qrcode = generate_qrcode_from_text(instance.user.username)
        instance.save()
        return Response(
            serializers.ArcherMemberSerializer(instance).data
        )

    @action(methods=['DELETE'], detail=True)
    def reject(self, request, pk=None):
        instance = self.get_object()
        if instance.delete():
            instance.user.delete()

        return Response(
            self.serializer_class(instance).data
        )


class RegionalViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    serializer_class = serializers.RegionalSerializer
    queryset = region_models.Region.objects.all()


class ProvinceViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    serializer_class = serializers.ProvinceSerializer
    queryset = region_models.Province.objects.all()

    def get_queryset(self):
        regional = self.request.query_params.get('regional')
        return super().get_queryset().filter(regional__pk=regional)


class BranchViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    serializer_class = serializers.BranchSerializer
    queryset = club_models.Branch.objects.all()

    def get_queryset(self):
        province = self.request.query_params.get('province')
        return super().get_queryset().filter(province__pk=province)


class ClubViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    serializer_class = serializers.OpenClubSerializer
    queryset = club_models.Club.objects.all()

    def get_queryset(self):
        branch = self.request.query_params.get('branch')
        return super().get_queryset().filter(branch__pk=branch)


class UnitViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    serializer_class = serializers.OpenUnitSerializer
    queryset = club_models.Unit.objects.all()

    def get_queryset(self):
        branch = self.request.query_params.get('branch')
        return super().get_queryset().filter(branch__pk=branch)


class ArcheryRangeViewSet(viewsets.ModelViewSet):
    permission_classes = [core_perm.IsGeneralUser]
    serializer_class = serializers.OpenArcheryRangeSerializer
    queryset = club_models.ArcheryRange.objects.all()

    def get_queryset(self):
        member = self.request.user.get_active_profile()
        if member.club:
            return super().get_queryset().filter(club=member.club)
        elif member.satuan:
            return super().get_queryset().filter(satuan=member.satuan)
