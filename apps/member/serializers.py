from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction
from django.db.utils import IntegrityError
from rest_framework import serializers

from core.exceptions import PerdanaError
from core.utils.permission_checker import get_user_group
from orm.models import member


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
            Token.objects.create(user=user)
        except IntegrityError:
            raise PerdanaError(message="User %s sudah digunakan" % user_data['username'])

        return member.ArcherMember.objects.create(user=user, **validated_data)
