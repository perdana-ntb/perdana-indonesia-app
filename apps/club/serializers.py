from rest_framework import serializers

from orm.models import club as club_models


class OpenClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = club_models.Club
        fields = '__all__'


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = club_models.Club
        fields = '__all__'

    # def update(self, instance, validated_data):
    #     return super().update(instance, validate_data)


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = club_models.Unit
        fields = '__all__'

    # def update(self, instance, validated_data):
    #     return super().update(instance, validate_data)
