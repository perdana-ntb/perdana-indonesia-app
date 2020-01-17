from django.shortcuts import render
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.
from apps.practice import serializers
from core import permissions
from core.exceptions import PerdanaError
from orm import practice


class TargetTypeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsClubOrSatuanManagerUser]
    serializer_class = serializers.TargetTypeSerializer
    queryset = practice.TargetType.objects.all()
    pagination_class = None


class PracticeViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsClubOrSatuanManagerUser]
    serializer_class = serializers.BasePracticeContainerSerializer
    queryset = practice.PracticeContainer.objects.all()
    http_method_names = ['get', 'post', ]

    def get_queryset(self):
        archer_id = self.request.query_params.get('archer_id', None)
        if not archer_id:
            raise PerdanaError(message='Pilih arhcer terlebih dahulu', status_code=status.HTTP_400_BAD_REQUEST)
        return super().get_queryset().filter(member__pk=archer_id)

    def retrieve(self, request, pk=None):
        return Response(serializers.PracticeContainerSerializer(self.get_object()).data)

    @action(detail=True, methods=['PUT', ], url_name='change-score', url_path='change-score', serializer_class=serializers.PracticeScoreSerializer)
    def change_score(self, request, pk=None):
        instance = practice.PracticeScore.objects.get(pk=pk)
        serializer = self.serializer_class(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(self.serializer_class(instance).data)

class ActivePracticeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.IsClubOrSatuanManagerUser]
    serializer_class = serializers.BasePracticeContainerSerializer
    queryset = practice.PracticeContainer.objects.filter(completed=False)

    def get_queryset(self):
        archer_id = self.request.query_params.get('archer_id', None)
        if not archer_id:
            raise PerdanaError(message='Pilih arhcer terlebih dahulu', status_code=status.HTTP_400_BAD_REQUEST)
        return super().get_queryset().filter(member__pk=archer_id)

    def get_object(self, **kwargs):
        qs = self.get_queryset().order_by('-pk')
        instance = qs.first()
        if qs.count() > 1:
            qs.exlcldue(pk=instance.pk).uppdate(completed=True)
        return instance

    def list(self, request):
        return Response(self.serializer_class(self.get_object()).data)
