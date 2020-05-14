# Create your views here.
from django.contrib.auth import authenticate
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import mixins, views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from club.models import Branch, ClubUnit
from core import permissions as core_perm
from core.exceptions import PerdanaError
from core.pagination import CustomPageNumberPagination
from core.permissions import PERDANA_USER_ROLE
from core.utils.generator import generate_qrcode_from_text
from core.utils.permission_checker import get_user_group
from member import serializers
from member.models import ArcherMember
from region.models import Province, Region


class LoginViewset(views.APIView):
    permission_classes = []
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = authenticate(**serializer.validated_data)
            if user:
                if hasattr(user, 'basemember'):
                    if hasattr(user.basemember, 'archermember'):
                        if not user.basemember.archermember.approved:
                            raise PerdanaError(message="User sedang dalam proses review oleh admin",
                                               status_code=403)

                    group = get_user_group(user)
                    return Response({
                        'token': user.auth_token.key,
                        'role': group if group else None,
                        'member': serializers.BaseArcherMemberSerializer(user.basemember).data
                    })
                raise PerdanaError(message="Jenis user tidak dapat melakukan aksi ini",
                                   status_code=403)
            raise PerdanaError(message="Username dan atau password salah", status_code=400)
        return Response(**serializer.validated_data, status=400)


class RegisterViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = []
    serializer_class = serializers.ArcherMemberSerializer


class UserProfileViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [core_perm.IsGeneralUser]

    def list(self, request):
        member = self.request.user.basemember
        if hasattr(member, 'archermember'):
            return Response(serializers.ArcherMemberSerializer(member.archermember).data)
        elif hasattr(member, 'clubunitcommitemember'):
            return Response(serializers.ClubUnitCommiteMemberSerializer(
                member.clubunitcommitemember).data
            )
        else:
            raise PerdanaError(message="Jenis user tidak dapat melakukan aksi ini")

    @action(detail=False, methods=['post'], permission_classes=[core_perm.IsGeneralUser])
    def change(self, request, pk=None):
        member = self.request.user.basemember
        if hasattr(member, 'archermember'):
            serializer = serializers.ArcherMemberSerializer(
                instance=member.archermember, data=request.data
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializers.ArcherMemberSerializer(member.archermember).data)
        elif hasattr(member, 'clubunitcommitemember'):
            serializer = serializers.ClubUnitCommiteMemberSerializer(
                instance=member.clubunitcommitemember, data=request.data
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializers.ClubUnitCommiteMemberSerializer(
                member.clubunitcommitemember
            ).data)
        else:
            raise PerdanaError(message="Jenis user tidak dapat melakukan aksi ini")


class ArcherMemberViewset(viewsets.ReadOnlyModelViewSet):
    permission_classes = [core_perm.IsGeneralUser]
    serializer_class = serializers.ArcherMemberSerializer
    queryset = ArcherMember.objects.filter(approved=True)
    pagination_class = CustomPageNumberPagination

    def get_queryset(self, **kwargs):
        user = self.request.user
        if user.groups.filter(name=PERDANA_USER_ROLE[0]).count() > 0:
            member = user.basemember.regionalcommitemember
            return super().get_queryset().filter(
                Q(club__branch__province__regional=member.regional) |
                Q(satuan__branch__province__regional=member.regional))
        elif user.groups.filter(name=PERDANA_USER_ROLE[1]).count() > 0:
            member = user.basemember.pengprovcommitemember
            return super().get_queryset().filter(
                Q(club__branch__province=member.province) |
                Q(satuan__branch__province=member.province))
        elif user.groups.filter(name=PERDANA_USER_ROLE[2]).count() > 0:
            member = user.basemember.pengcabcommitemember
            return super().get_queryset().filter(
                Q(club__branch=member.branch) |
                Q(satuan__branch=member.branch))
        elif user.groups.filter(name=PERDANA_USER_ROLE[3]).count() > 0:
            member = user.basemember.clubunitcommitemember
            if member.club:
                return super().get_queryset().filter(club=member.club)
            elif member.satuan:
                return super().get_queryset().filter(satuan=member.satuan)
        else:
            return super().get_queryset().filter(pk=user.basemember.archermember.pk)

    @action(detail=True, methods=['put'], permission_classes=[core_perm.IsClubOrSatuanManagerUser])
    def change(self, request, pk=None):
        instance = get_object_or_404(ArcherMember, pk=self.kwargs.get('pk'))
        serializer = self.serializer_class(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(self.serializer_class(instance).data)

    @action(detail=True, methods=['get'], permission_classes=[core_perm.IsClubOrSatuanManagerUser])
    def approve(self, request, pk=None):
        obj = get_object_or_404(ArcherMember, pk=self.kwargs.get('pk'))
        obj.approved = True
        obj.approved_by = self.request.user

        obj.qrcode = generate_qrcode_from_text(obj.user.Username)
        obj.save()
        return Response(self.serializer_class(obj).data)

    @action(detail=False, methods=['get'], permission_classes=[core_perm.IsClubOrSatuanManagerUser])
    def applicants(self, request):
        try:
            member = self.request.user.basemember.clubunitcommitemember
            qs = ArcherMember.objects.filter(approved=False)
            if member.club:
                qs = qs.filter(club=member.club)
            elif member.satuan:
                qs = qs.filter(satuan=member.satuan)

            return Response(self.serializer_class(qs, many=True).data)
        except AttributeError:
            raise PerdanaError(message='User belum memiliki klub atau satuan')


class RegionalViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    serializer_class = serializers.RegionalSerializer
    queryset = Region.objects.all()


class ProvinceViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    serializer_class = serializers.ProvinceSerializer
    queryset = Province.objects.all()

    def get_queryset(self):
        regional = self.request.query_params.get('regional')
        return super().get_queryset().filter(regional__pk=regional)


class BranchViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    serializer_class = serializers.BranchSerializer
    queryset = Branch.objects.all()

    def get_queryset(self):
        province = self.request.query_params.get('province')
        return super().get_queryset().filter(province__pk=province)


class ClubUnitViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    serializer_class = serializers.OpenClubUnitSerializer
    queryset = ClubUnit.objects.all()

    def get_queryset(self):
        branch = self.request.query_params.get('branch')
        return super().get_queryset().filter(branch__pk=branch)
