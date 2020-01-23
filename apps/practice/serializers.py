from django.db.models import Sum
from django.db.utils import IntegrityError
from django.forms.models import model_to_dict
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
    id = serializers.CharField()

    class Meta:
        model = practice.PracticeScore
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
        model = practice.PracticeSeries
        fields = '__all__'


class BasePracticeContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = practice.PracticeContainer
        exclude = ['status', 'signed', 'signed_by']

    def to_representation(self, instance):
        reps = super().to_representation(instance)
        practice_series = instance.practice_series.order_by('serie')
        reps['total'] = practice_series.aggregate(socre_total=Sum('total'))['socre_total']
        return reps

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
