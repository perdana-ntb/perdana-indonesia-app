from django.urls import path

from club.views import ClubAddFormView, ClubListView, RegionalClubJsonView

urlpatterns = [
    path('regional-clubs/<str:region_id>', RegionalClubJsonView.as_view(), name='regional-club'),
    path('clubs', ClubListView.as_view(), name='clubs'),
    path('club-dd', ClubAddFormView.as_view(), name='club-add')
]
