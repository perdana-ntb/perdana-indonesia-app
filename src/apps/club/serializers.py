from rest_framework import serializers

from club.models import ArcheryRange, ClubUnit


class ClubUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubUnit
        fields = '__all__'


class ArcheryRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArcheryRange
        fields = "__all__"

    def to_respresentation(self, instance):
        reps = super().to_respresentation(instance)
        reps['managed_by'] = ClubUnitSerializer(instance.managed_by).data
        return reps
