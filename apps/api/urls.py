from django.urls import path, include

urlpatterns = [
    path('member/', include(('apps.member.urls', 'member_api'), namespace='member_api')),
    path('org/', include(('apps.club.urls', 'org_api'), namespace='org_api')),
]
