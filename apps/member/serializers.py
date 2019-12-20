from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, User
from django.db import transaction
from django.db.utils import IntegrityError
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from core.exceptions import PerdanaError
from core.permissions import PERDANA_USER_ROLE
from core.utils.permission_checker import get_user_group
from orm.models import club as club_models
from orm.models import member
from orm.models import region as region_models


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']


class BaseArcherMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = member.ArcherMember
        fields = ['phone', 'gender', 'address', 'photo', 'qrcode']

    def to_representation(self, instance):
        reps = super().to_representation(instance)
        if instance.club:
            reps['club'] = {
                'id': instance.club.pk,
                'name': instance.club.name,
            }

        if instance.satuan:
            reps['satuan'] = {
                'id': instance.satuan.pk,
                'name': instance.satuan.name,
            }
        return reps


class ArcherMemberSerializer(BaseArcherMemberSerializer):
    user = UserSerializer()

    class Meta:
        model = member.ArcherMember
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        try:
            user = User.objects.create_user(**user_data)
            group = Group.objects.get(name=PERDANA_USER_ROLE[4])

            user.groups.add(group)
            Token.objects.create(user=user)
        except Group.DoesNotExist:
            raise PerdanaError(message="Member group %s tidak ditemukan" % PERDANA_USER_ROLE[4])
        except IntegrityError:
            raise PerdanaError(message="User %s sudah digunakan" % user_data['username'])

        return member.ArcherMember.objects.create(user=user, **validated_data)


class RegionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = region_models.Region
        fields = ['id', 'name']


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = region_models.Province
        fields = ['id', 'name']


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = club_models.Branch
        fields = ['id', 'name']


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = club_models.Club
        fields = ['id', 'name']


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = club_models.Unit
        fields = ['id', 'name']
