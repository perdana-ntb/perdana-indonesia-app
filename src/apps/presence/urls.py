from rest_framework.routers import DefaultRouter

from . import viewsets

router = DefaultRouter(trailing_slash=True)
router.register('list', viewsets.PresenceContainerViewSet, basename='presence')

urlpatterns = []

urlpatterns += router.urls
