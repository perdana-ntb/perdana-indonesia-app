from django.urls import path

from .views import DashboardTemplateView

urlpatterns = [
    path('main', DashboardTemplateView.as_view(), name='main')
]
