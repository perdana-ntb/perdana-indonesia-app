from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter(trailing_slash=True)
router.register('apps', views.AppMenuViewSet, basename='app-menu')

urlpatterns = [
]

urlpatterns += router.urls
