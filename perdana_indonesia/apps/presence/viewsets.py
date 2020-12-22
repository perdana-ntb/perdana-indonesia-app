from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.exceptions import PerdanaError
from core.permissions import IsClubOrSatuanManagerUser

from . import serializers
from .models import PresenceContainer, PresenceItem

# Create your views here.


class PresenceContainerViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BasePresenceContainerSerializer
    permission_classes = [IsClubOrSatuanManagerUser]
    queryset = PresenceContainer.objects.all()

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
        user = self.request.query_params.get('user')
        status = self.request.query_params.get('status')
        try:
            item_obj = obj.presence_items.get(member__user__username=user)
            item_obj.status = status
            item_obj.save()
            return Response(serializers.PresenceItemSerializer(item_obj).data)
        except PresenceItem.DoesNotExist:
            raise PerdanaError(message="PresenceItem tidak ditemukan")
