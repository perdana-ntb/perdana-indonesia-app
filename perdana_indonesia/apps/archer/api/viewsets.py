from archer.api.serializers import ArcherSerializer, LoginSerializer
from archer.models import Archer
from core.exceptions import PerdanaError
from core.permissions import IsGeneralUser
from django.contrib.auth.models import AnonymousUser, User
from rest_framework import mixins, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class LoginViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (AllowAny, )
    serializer_class = LoginSerializer

    def getUserByUsername(self, username: str) -> User:
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise PerdanaError(
                message='Username dan atau password salah',
                status_code=404
            )

    def validateUserPasswordIsMatched(self, user: User, password: str) -> None:
        if not user.check_password(password):
            raise PerdanaError(
                message='Password yang anda masukkan salah',
                status_code=400
            )

    def validateUserHasArcherObject(self, user: User) -> None:
        if not hasattr(user, 'archer') and not user.archer:
            raise PerdanaError(
                message='Jenis user tidak diizinkan',
                status_code=403
            )

    def validateUserIsApproved(self, user: User) -> None:
        if not user.archer.approved:
            raise PerdanaError(
                message='Akun masih dalam tahan review oleh pengurus',
                status_code=403
            )

    def validateUserIsActive(self, user: User) -> None:
        if not user.archer.is_active:
            raise PerdanaError(
                message='Akun tidak aktif, silahkan menghubungi pengurus club',
                status_code=403
            )

    def createAuthTokenIfNoExist(self, user: User) -> Token:
        token, _ = Token.objects.get_or_create(user=user)
        return token

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username, password = serializer.validated_data.values()
        user: User = self.getUserByUsername(username)
        self.validateUserPasswordIsMatched(user, password)
        self.validateUserHasArcherObject(user)
        self.validateUserIsApproved(user)
        self.validateUserIsActive(user)
        token = self.createAuthTokenIfNoExist(user)

        return Response({
            'token': token.key,
            'user': {
                'username': user.username,
                'group': user.groups.first().name,
                'full_name': user.archer.full_name
            }
        })


class ArhcerProfileViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsGeneralUser, )
    serializer_class = ArcherSerializer
    queryset = Archer.objects.filter(is_active=True, approved=True)

    def list(self, request, *args, **kwargs):
        return Response(self.serializer_class(request.user.archer).data)


class ArhcerCheckMembershipViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (AllowAny, )
    serializer_class = ArcherSerializer
    queryset = Archer.objects.filter(is_active=True, approved=True)

    def getResponseData(self, archer: Archer):
        if isinstance(self.request.user, AnonymousUser):
            return {
                'archer_id': archer.user.username,
                'full_name': archer.full_name,
                'date_register': archer.date_register,
                'is_active': archer.is_active,
                'club': archer.club.name
            }
        else:
            return self.serializer_class(archer).data

    def list(self, request, *args, **kwargs):
        archerId = self.request.query_params.get('archer_id')
        if not archerId:
            raise PerdanaError(
                message='Sertakan archer_id sebagai query params',
                status_code=400
            )
        try:
            instance = self.get_queryset().get(user__username=archerId)
            return Response(self.getResponseData(instance))
        except Archer.DoesNotExist:
            raise PerdanaError(
                message='Id %s tidak ditemukan' % archerId,
                status_code=404
            )
