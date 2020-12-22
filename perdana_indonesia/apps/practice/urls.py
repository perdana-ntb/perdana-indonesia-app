from django.urls import path
from rest_framework.routers import DefaultRouter

from . import viewsets

router = DefaultRouter(trailing_slash=True)
router.register('containers', viewsets.PracticeContainerViewSet, basename='practice')
router.register('series', viewsets.UpdateScoreViewSet, basename='series')
router.register('target', viewsets.TargetTypeViewSet, basename='target')
router.register('nearest-practices', viewsets.NearestPracticeViewSet, basename='nearest-practices')

urlpatterns = [
    path('active', viewsets.ActivePracticeViewSet.as_view({'get': 'list'}), name='active'),
]

urlpatterns += router.urls
