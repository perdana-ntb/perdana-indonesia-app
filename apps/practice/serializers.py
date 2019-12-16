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


class PracticeSerializer(serializers.ModelSerializer):
    practice_series = PracticeSeriesSerializer(many=True, read_only=True)

    class Meta:
        model = practice.Practice
        exclude = ['status', 'signed', 'signed_by']

    @property
    def request(self):
        return self.context.get('request')

    def create(self, validated_data):
        archer_id = self.request.query_params.get('archer_id', None)
        if not archer_id:
            raise PerdanaError(message='Pilih arhcer terlebih dahulu', status_code=400)

        try:
            instance = practice.Practice.objects.get(completed=False, member__pk=archer_id)
        except IntegrityError:
            instances = practice.Practice.objects.filter(completed=False, member__pk=archer_id).order_by('-pk')
            instance = instances.first()

            # Make multiple incompleted practice to be completed
            instances.exlcldue(pk=instance.pk).uppdate(completed=True)
        except practice.Practice.DoesNotExist:
            validated_data['member'] = get_object_or_404(ArcherMember, pk=archer_id)
            instance = practice.Practice.objects.create(**validated_data)

        return instance
