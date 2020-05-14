from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from club.serializers import ArcheryRangeSerializer
from core.exceptions import PerdanaError
from member.models import ArcherMember

from .models import (PracticeContainer, PracticeSchedule, PracticeScore,
                     PracticeSeries, TargetType)


class TargetTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetType
        fields = '__all__'


class PracticeScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = PracticeScore
        exclude = ['serie', ]


class PracticeSeriesScoreSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    total = serializers.IntegerField(read_only=True)
    serie = serializers.IntegerField(read_only=True)
    closed = serializers.BooleanField(read_only=True)
    scores = PracticeScoreSerializer(many=True)

    def update(self, instance, validated_data):
        scores = validated_data.get('scores')
        for score in scores:
            score_obj = instance.scores.get(pk=score['id'])
            score_obj.score = score['score']
            score_obj.filled = score['filled']
            score_obj.save()

        # trigger save method
        instance.closed = True
        instance.save()

        if instance.practice_container.practice_series.filter(closed=False).count() == 0:
            instance.practice_container.completed = True
            instance.practice_container.save()

        return instance


class PracticeSeriesSerializer(serializers.ModelSerializer):
    scores = PracticeScoreSerializer(many=True, read_only=True)

    class Meta:
        model = PracticeSeries
        fields = '__all__'


class BasePracticeContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PracticeContainer
        exclude = ['status', 'signed', 'signed_by']

    @property
    def request(self):
        return self.context.get('request')

    def create(self, validated_data):
        archer_id = self.request.query_params.get('archer', None)
        if not archer_id:
            raise PerdanaError(message='Pilih arhcer terlebih dahulu', status_code=400)

        try:
            instance = PracticeContainer.objects.get(completed=False, member__pk=archer_id)
            raise PerdanaError(message="Selesaikan skoring yang telah berjalan terlebih dahulu")
        except IntegrityError:
            instances = PracticeContainer.objects.filter(completed=False, member__pk=archer_id)\
                .order_by('-pk')
            instance = instances.first()

            # Make multiple incompleted practice to be completed
            instances.exlcldue(pk=instance.pk).update(completed=True)
            raise PerdanaError(message="Selesaikan skoring yang telah berjalan terlebih dahulu")
        except PracticeContainer.DoesNotExist:
            validated_data['member'] = get_object_or_404(ArcherMember, pk=archer_id)
            instance = PracticeContainer.objects.create(**validated_data)

        return instance


class PracticeContainerSerializer(BasePracticeContainerSerializer):
    practice_series = PracticeSeriesSerializer(many=True, read_only=True)


class PracticeScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PracticeSchedule
        fields = '__al__'


class NearestPracticeScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PracticeSchedule
        fields = "__all__"

    def to_representation(self, instance):
        reps = super().to_representation(instance)
        reps['archery_range'] = ArcheryRangeSerializer(instance.archery_range).data
        reps['day_display'] = instance.get_day_display()
        reps['distance'] = instance.distance
        return reps
