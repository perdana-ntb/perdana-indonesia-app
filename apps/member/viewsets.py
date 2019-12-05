# Create your views here.
from orm.models import member
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from core.utils.generator import generate_qrcode_from_text
from rest_framework import viewsets, views
from rest_framework import mixins, status
from apps.member import serializers
from rest_framework.response import Response
from core.exceptions import PerdanaError
from core import permissions as core_perm

from django.contrib.auth import authenticate
from core.utils.permission_checker import get_user_group


class LoginViewset(views.APIView):
    permission_classes = []
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = authenticate(**serializer.validated_data)
            if user:
                if hasattr(user, 'member'):
                    group = get_user_group(user)
                    return Response({
                        'token': user.auth_token.key,
                        'role': group if group else None,
                        'member': serializers.BaseArcherMemberSerializer(user.member).to_representation(user.member)
                    })
            raise PerdanaError(message="Jenis user tidak dapat melakukan aksi ini", status_code=503)
        raise PerdanaError(message="Username dan atau password salah")

        return Response(**serializer.validated_data)
        raise PerdanaError(message="Username dan atau password salah")


class RegisterViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = []
    serializer_class = serializers.ArcherMemberSerializer


class ArcherMemberViewset(viewsets.ReadOnlyModelViewSet):
    permission_classes = [core_perm.IsClubOrSatuanManagerUser]
    serializer_class = serializers.ArcherMemberSerializer
    queryset = member.ArcherMember.objects.filter(approved=True)

    def get_queryset(self, **kwargs):
        member = self.request.user.member
        if member.club:
            return super().get_queryset().filter(club=member.club)
        else:
            return super().get_queryset().filter(satuan=member.satuan)
