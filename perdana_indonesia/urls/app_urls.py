from django.urls import include, path

urlpatterns = [
    path('dashboard/', include(('dashboardd.urls', 'dashboardd'), namespace='dashboardd')),
    path('archer/', include(('archer.urls', 'archer'), namespace='archer')),
    path('organisation/', include(('club.urls', 'club'), namespace='club')),
    path('region/', include(('region.urls', 'region'), namespace='region')),
]
