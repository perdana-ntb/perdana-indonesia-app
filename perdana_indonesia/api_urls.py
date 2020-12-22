from django.urls import include, path

urlpatterns = [
    path('organisation/', include(('club.urls', 'org_api'), namespace='org_api')),
    path('practices/', include(('practice.urls', 'practice_api'), namespace='practice_api')),
    path('presences/', include(('presence.urls', 'presence_api'), namespace='presence_api')),
    path('menu/', include(('menu.urls', 'menu_api'), namespace='menu_api')),
]
