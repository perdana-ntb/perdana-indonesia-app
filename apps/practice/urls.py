from django.urls import path
from apps.practice import viewsets
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=True)
router.register('list', viewsets.PracticeViewSet, basename='practice')
router.register('series', viewsets.UpdateScoreViewSet, basename='serie')
router.register('target', viewsets.TargetTypeViewSet, basename='target')

urlpatterns = [
    path('active', viewsets.ActivePracticeViewSet.as_view({'get': 'list'}), name='active'),
]

urlpatterns += router.urls
