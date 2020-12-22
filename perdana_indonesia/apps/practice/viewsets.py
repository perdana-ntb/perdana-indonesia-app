from django.db.models import CharField, F, FloatField, Value
from django.utils import timezone
from rest_framework import mixins, viewsets
from rest_framework.response import Response

from core import haversine, permissions
from core.exceptions import PerdanaError
from core.pagination import CustomPageNumberPagination

# Create your views here.
from . import serializers
from .models import (PracticeContainer, PracticeSchedule, PracticeSeries,
                     TargetType)


class TargetTypeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsClubOrSatuanManagerUser]
    serializer_class = serializers.TargetTypeSerializer
    queryset = TargetType.objects.all()
    pagination_class = None


class PracticeContainerViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsGeneralUser]
    serializer_class = serializers.BasePracticeContainerSerializer
    queryset = PracticeContainer.objects.all()
    http_method_names = ['get', 'post', ]

    def get_queryset(self):
        archer_id = self.request.query_params.get('archer_id', None)
        if not archer_id:
            raise PerdanaError(message='Pilih arhcer terlebih dahulu', status_code=400)
        return super().get_queryset().filter(member__pk=archer_id)

    def retrieve(self, request, pk=None):
        return Response(serializers.PracticeContainerSerializer(self.get_object()).data)

    # @action(detail=True, methods=['PUT', ], url_name='change-score',
    # url_path='change-score', serializer_class=serializers.PracticeSeriesScoreSerializer)
    # def change_score(self, request, pk=None):
    #     instance = PracticeScore.objects.get(pk=pk)
    #     serializer = self.serializer_class(instance=instance, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()

        # return Response(self.serializer_class(instance).data)


class UpdateScoreViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.IsGeneralUser]
    serializer_class = serializers.PracticeSeriesScoreSerializer

    def get_object(self):
        return PracticeSeries.objects.get(pk=self.kwargs.get('pk'))


class ActivePracticeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.IsClubOrSatuanManagerUser]
    serializer_class = serializers.BasePracticeContainerSerializer
    queryset = PracticeContainer.objects.filter(completed=False)

    def get_queryset(self):
        archer_id = self.request.query_params.get('archer_id', None)
        if not archer_id:
            raise PerdanaError(message='Pilih arhcer terlebih dahulu', status_code=400)
        return super().get_queryset().filter(member__pk=archer_id)

    def get_object(self, **kwargs):
        qs = self.get_queryset().order_by('-pk')
        instance = qs.first()
        if qs.count() > 1:
            qs.exlcldue(pk=instance.pk).uppdate(completed=True)
        return instance

    def list(self, request):
        return Response(self.serializer_class(self.get_object()).data)


class NearestPracticeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.IsGeneralUser, )
    serializer_class = serializers.NearestPracticeScheduleSerializer
    pagination_class = CustomPageNumberPagination
    queryset = PracticeSchedule.objects.all()
    NEAREST_PRACTICE_CHOICES = ['all', 'open']

    def get_annoted_queryset(self, queryset):
        try:
            latitude, longitude = self.request.query_params.get('coordinate').split(',')
            return queryset.annotate(
                user_latitude=Value(latitude, output_field=FloatField()),
                user_longitude=Value(longitude, output_field=FloatField()),
                latitude=F("archery_range__latitude"),
                longitude=F("archery_range__longitude"),
                distance=Value(
                    haversine.calculate_distance(),
                    output_field=CharField()
                )).order_by('distance')
        except (TypeError, KeyError):
            return super().get_queryset()

    def get_queryset(self):
        if 'coordinate' not in self.request.query_params:
            return super().get_queryset()
        try:
            queryset = self.get_annoted_queryset(super().get_queryset())
            if 'query_type' not in self.request.query_params:
                raise PerdanaError(message="Pass query_type in query_params")

            query_type = self.request.query_params.get('query_type')
            if query_type == self.NEAREST_PRACTICE_CHOICES[0]:
                return queryset
            elif query_type == self.NEAREST_PRACTICE_CHOICES[1]:
                now = timezone.now()
                return queryset.filter(
                    day=now.weekday(), start_time__lte=now.time(), end_time__gte=now.time()
                )
            else:
                raise PerdanaError(message="Please pass query_type with the correct value")
        except (TypeError, KeyError):
            return super().get_queryset()

    def list(self, request):
        paginated_queryset = self.paginate_queryset(self.get_queryset())
        return self.get_paginated_response(
            self.serializer_class(paginated_queryset, many=True).data
        )
