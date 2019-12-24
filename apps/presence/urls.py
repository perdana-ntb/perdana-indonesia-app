from django.urls import path
from apps.presence import viewsets
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=True)
router.register('list', viewsets.PresenceContainerViewSet, basename='presence')

urlpatterns = []

urlpatterns += router.urls
