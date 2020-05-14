from django.contrib.auth.models import Group, User
from django.db import transaction
from django.db.utils import IntegrityError
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from club.models import Branch, ClubUnit
from commite.models import ClubUnitCommiteMember
from core.exceptions import PerdanaError
from core.permissions import PERDANA_USER_ROLE
from member.models import ArcherMember
from region.models import Province, Region


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']
        validators = []


class ClubUnitCommiteMemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, allow_blank=True)

    class Meta:
        model = ClubUnitCommiteMember
        fields = '__all__'

    def update(self, instance, validated_data):
        username = validated_data.pop('username')
        try:
            user = instance.user
            user.username = username
            user.save()
        except User.DoesNotExist:
            raise PerdanaError(message="Member %s tidak ditemukan" % username)
        except IntegrityError:
            raise PerdanaError(message="User %s sudah digunakan" % username)

        return super().update(instance, validated_data)


class BaseArcherMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArcherMember
        fields = ['phone', 'gender', 'address', 'photo', 'qrcode']

    def to_representation(self, instance):
        reps = super().to_representation(instance)
        if instance.clubunit:
            reps['clubunit'] = {
                'id': instance.clubunit.pk,
                'name': instance.clubunit.name,
            }
        return reps


class ArcherMemberSerializer(BaseArcherMemberSerializer):
    user = UserSerializer(read_only=True)
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, allow_blank=True)

    class Meta:
        model = ArcherMember
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        try:
            user = User.objects.create_user(username=username, password=password)
            group = Group.objects.get(name=PERDANA_USER_ROLE[4])

            user.groups.add(group)
            Token.objects.create(user=user)
        except Group.DoesNotExist:
            raise PerdanaError(message="Member group %s tidak ditemukan" % PERDANA_USER_ROLE[4])
        except IntegrityError:
            raise PerdanaError(message="User %s sudah digunakan" % username)

        return ArcherMember.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        username = validated_data.pop('username')
        try:
            user = instance.user
            user.username = username
            user.save()
        except User.DoesNotExist:
            raise PerdanaError(message="Member %s tidak ditemukan" % username)
        except IntegrityError:
            raise PerdanaError(message="User %s sudah digunakan" % username)

        return super().update(instance, validated_data)


class RegionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name']


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['id', 'name']


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id', 'name']


class OpenClubUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubUnit
        fields = ['id', 'name']
