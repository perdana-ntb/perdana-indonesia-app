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
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']


class BaseArcherMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = member.ArcherMember
        fields = ['phone', 'gender', 'address', 'photo', 'qrcode']

    def to_representation(self, instance):
        reps = super().to_representation(instance)
        reps['club'] = {
            'id': instance.club.pk,
            'name': instance.club.name,
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
        except IntegrityError:
            raise PerdanaError(message="User %s sudah digunakan" % user_data['username'])

        member = member.ArcherMember.objects.create(user=user, **validated_data)
        return member
