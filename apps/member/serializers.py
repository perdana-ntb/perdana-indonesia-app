from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import Group
from django.db import transaction
from django.db.utils import IntegrityError
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from core.exceptions import PerdanaError
from core.permissions import PERDANA_USER_ROLE
from core.utils.permission_checker import get_user_group
from orm import commite
from orm.models import club as club_models
from orm.models import member
from orm.models import region as region_models

USER = get_user_model()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = USER
        fields = ['username', 'password']
        validators = []


class ClubUnitCommiteMemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, allow_blank=True)

    class Meta:
        model = commite.ClubUnitCommiteMember
        fields = '__all__'

    def update(self, instance, validated_data):
        username = validated_data.pop('username')
        try:
            user = instance.user
            user.username = username
            user.save()
        except USER.DoesNotExist:
            raise PerdanaError(message="Member %s tidak ditemukan" % username)
        except IntegrityError:
            raise PerdanaError(message="USER %s sudah digunakan" % username)

        return super().update(instance, validated_data)


class BaseArcherMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = member.ArcherMember
        fields = ['id', 'phone', 'gender', 'address', 'photo', 'qrcode']

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


class RegisterSerializer(BaseArcherMemberSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, allow_blank=True)
    qrcode = serializers.CharField(read_only=True)

    class Meta:
        model = member.ArcherMember
        exclude = ['user', 'approved', 'approved_by', 'religion', 'verified', 'status', 'physic_information', 'closed', ]

    @transaction.atomic
    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        try:
            user = USER.objects.create_user(username=username, password=password)
            group = Group.objects.get(name=PERDANA_USER_ROLE[4])

            user.groups.add(group)
            Token.objects.create(user=user)
        except Group.DoesNotExist:
            raise PerdanaError(message="Member group %s tidak ditemukan" % PERDANA_USER_ROLE[4])
        except IntegrityError:
            raise PerdanaError(message="USER %s sudah digunakan" % username)

        return member.ArcherMember.objects.create(user=user, **validated_data)


class ArcherMemberProfileUpdateSerializer(serializers.Serializer):
    gender = serializers.CharField()
    blood_type = serializers.CharField()
    disease_history = serializers.CharField()
    photo = serializers.ImageField(required=False)
    public_photo = serializers.ImageField(required=False)

    body_height = serializers.CharField()
    body_weight = serializers.CharField()
    draw_length = serializers.CharField()

    def update(self, instance, validated_data):
        if instance.physic_information:
            instance.physic_information.body_height = validated_data.pop('body_height')
            instance.physic_information.body_weight = validated_data.pop('body_weight')
            instance.physic_information.draw_length = validated_data.pop('draw_length')
            instance.physic_information.save()
        else:
            physic_information = member.PhysicInformation.objects.create(body_height=validated_data.pop('body_height'),
                                                                         body_weight=validated_data.pop('body_weight'),
                                                                         draw_length=validated_data.pop('draw_length'))
            instance.physic_information = physic_information
            instance.save()

        if validated_data.get('gender', instance.gender) == member.GENDER_CHOICES[0][0]:
            instance.photo = validated_data.pop('photo')
            instance.public_photo = instance.photo
        else:
            instance.photo = validated_data.pop('photo')
            instance.public_photo = validated_data.pop('public_photo')

        instance.save()
        members = member.ArcherMember.objects.filter(pk=instance.pk)
        members.update(**validated_data)

        return instance

class ApproveArcherMemberSerializer(serializers.Serializer):
    register_number = serializers.CharField()

class ArcherMemberSerializer(BaseArcherMemberSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = member.ArcherMember
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        try:
            user = USER.objects.create_user(username=username, password=password)
            group = Group.objects.get(name=PERDANA_USER_ROLE[4])

            user.groups.add(group)
            Token.objects.create(user=user)
        except Group.DoesNotExist:
            raise PerdanaError(message="Member group %s tidak ditemukan" % PERDANA_USER_ROLE[4])
        except IntegrityError:
            raise PerdanaError(message="USER %s sudah digunakan" % username)

        return member.ArcherMember.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        username = validated_data.pop('username')
        try:
            user = instance.user
            user.username = username
            user.save()
        except USER.DoesNotExist:
            raise PerdanaError(message="Member %s tidak ditemukan" % username)
        except IntegrityError:
            raise PerdanaError(message="USER %s sudah digunakan" % username)

        return super().update(instance, validated_data)


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


class OpenClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = club_models.Club
        fields = ['id', 'name']


class OpenUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = club_models.Unit
        fields = ['id', 'name']


class OpenArcheryRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = club_models.ArcheryRange
        fields = '__all__'
