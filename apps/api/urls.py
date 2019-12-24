from django.urls import path, include

urlpatterns = [
    path('user/', include(('apps.member.urls', 'user_api'), namespace='user_api')),
    path('org/', include(('apps.club.urls', 'org_api'), namespace='org_api')),
    path('practices/', include(('apps.practice.urls', 'practice_api'), namespace='practice_api')),
    path('presences/', include(('apps.presence.urls', 'presence_api'), namespace='presence_api')),
]
