from django.urls import include, path

urlpatterns = [
    path('archer/', include(('archer.api.urls', 'archer_api'), namespace='archer_api')),
]
