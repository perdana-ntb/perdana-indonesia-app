from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from core.exceptions import PerdanaError
from orm import practice
from orm.member import ArcherMember


class TargetTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = practice.TargetType
        fields = '__all__'


class PracticeScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = practice.PracticeScore
        fields = '__all__'


class PracticeSeriesSerializer(serializers.ModelSerializer):
    scores = PracticeScoreSerializer(many=True, read_only=True)

    class Meta:
        model = practice.PracticeSeries
        fields = '__all__'


class BasePracticeContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = practice.PracticeContainer
        exclude = ['status', 'signed', 'signed_by']

    @property
    def request(self):
        return self.context.get('request')

    def create(self, validated_data):
        archer_id = self.request.query_params.get('archer_id', None)
        if not archer_id:
            raise PerdanaError(message='Pilih arhcer terlebih dahulu', status_code=400)

        try:
            instance = practice.PracticeContainer.objects.get(completed=False, member__pk=archer_id)
            raise PerdanaError(message="Selesaikan skoring yang telah berjalan terlebih dahulu")
        except IntegrityError:
            instances = practice.PracticeContainer.objects.filter(completed=False, member__pk=archer_id).order_by('-pk')
            instance = instances.first()

            # Make multiple incompleted practice to be completed
            instances.exlcldue(pk=instance.pk).update(completed=True)
            raise PerdanaError(message="Selesaikan skoring yang telah berjalan terlebih dahulu")
        except practice.PracticeContainer.DoesNotExist:
            validated_data['member'] = get_object_or_404(ArcherMember, pk=archer_id)
            instance = practice.PracticeContainer.objects.create(**validated_data)

        return instance


class PracticeContainerSerializer(BasePracticeContainerSerializer):
    practice_series = PracticeSeriesSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        reps = super().to_representation(instance)
        practice_series = instance.practice_series.order_by('serie')
        reps['practice_series'] = PracticeSeriesSerializer(practice_series, many=True).data
        return reps
