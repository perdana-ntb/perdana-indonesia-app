from django.urls import path

from .views import (DashboardPengcabTemplateView,
                    DashboardPengprovTemplateView, DashboardPuslatTemplateView,
                    DashboardRouterView)

urlpatterns = [
    path('router', DashboardRouterView.as_view(), name='router'),
    path('puslat', DashboardPuslatTemplateView.as_view(), name='puslat'),
    path('pengcab', DashboardPengcabTemplateView.as_view(), name='pengcab'),
    path('pengprov', DashboardPengprovTemplateView.as_view(), name='pengprov'),
]
