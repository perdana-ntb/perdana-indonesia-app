from rest_framework import routers

from club.viewsets import ClubUnitViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('clubunits', ClubUnitViewSet)

urlpatterns = []
urlpatterns += router.urls
