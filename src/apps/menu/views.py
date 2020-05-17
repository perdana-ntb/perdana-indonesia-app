from rest_framework import viewsets

from core.permissions import IsGeneralUser

from .models import AppMenu
from .serializers import AppMenuSerializer


class AppMenuViewSet(viewsets.ModelViewSet):
    permission_classes = (IsGeneralUser, )
    serializer_class = AppMenuSerializer
    queryset = AppMenu.objects.filter(published=True)

    def get_queryset(self):
        return super().get_queryset().filter(allowed_groups__in=self.request.user.groups.all())
