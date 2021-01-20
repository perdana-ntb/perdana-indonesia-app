from django.urls import path

from .views import (DashboardPengcabTemplateView, DashboardPuslatTemplateView,
                    DashboardRouterView)

urlpatterns = [
    path('router', DashboardRouterView.as_view(), name='router'),
    path('puslat', DashboardPuslatTemplateView.as_view(), name='puslat'),
    path('pengcab', DashboardPengcabTemplateView.as_view(), name='pengcab'),
]
