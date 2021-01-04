from archer.models import Archer
from club.api.serializers import ClubSerializer
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class ArcherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Archer
        exclude = ('user', )

    def to_representation(self, instance):
        reps = super().to_representation(instance)
        reps['username'] = instance.user.username
        reps['club'] = ClubSerializer(instance.club).data
        return reps
