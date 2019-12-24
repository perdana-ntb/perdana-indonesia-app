from rest_framework import viewsets
from apps.presence import serializers
from core.permissions import IsClubOrSatuanManagerUser
from orm import presence as presence_models
# Create your views here.

from core.exceptions import PerdanaError
from rest_framework.response import Response
from rest_framework.decorators import action


class PresenceContainerViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BasePresenceContainerSerializer
    permission_classes = [IsClubOrSatuanManagerUser]
    queryset = presence_models.PresenceContainer.objects.all()

    def get_serializer_context(self, **kwargs):
        ctx = super().get_serializer_context(**kwargs)
        ctx['request'] = self.request
        return ctx

    def get_queryset(self):
        member = self.request.user.member
        if member.club:
            return super().get_queryset().filter(club=member.club)
        elif member.satuan:
            return super().get_queryset().filter(satuan=member.satuan)
        else:
            raise PerdanaError(message="Jenis akun tidak diizinkan untuk melakukan aksi ini")

    def retrieve(self, request, pk=None):
        return Response(serializers.PresenceContainerSerializer(self.get_object()).data)

    @action(detail=True, methods=['GET', ], url_name='change-status', url_path='change-status')
    def change_status(self, request, pk=None):
        obj = self.get_object()
        item = self.request.query_params.get('item')
        status = self.request.query_params.get('status')
        try:
            item_obj = obj.presence_items.get(pk=item)
            item_obj.status = status
            item_obj.save()
            return Response(serializers.PresenceItemSerializer(item_obj).data)
        except presence_models.PresenceItem.DoesNotExist:
            raise PerdanaError(message="PresenceItem tidak ditemukan")
