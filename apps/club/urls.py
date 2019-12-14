from django.urls import path
from rest_framework import routers

from apps.club import viewsets

router = routers.DefaultRouter(trailing_slash=False)
router.register('clubs', viewsets.ClubViewSet)
router.register('units', viewsets.UnitViewSet)

urlpatterns = []
urlpatterns += router.urls
