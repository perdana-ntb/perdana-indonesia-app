from django.urls import path

from .views import RegionalClubJsonView

urlpatterns = [
    path('regional-clubs/<str:region_id>', RegionalClubJsonView.as_view(), name='regional-club')
]
