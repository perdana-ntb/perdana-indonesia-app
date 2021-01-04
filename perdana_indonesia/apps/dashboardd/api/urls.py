from dashboardd.api.viewsets import DashboardViewSet
from django.urls.conf import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    path('main', DashboardViewSet.as_view(), name='main')
]
urlpatterns += router.urls
