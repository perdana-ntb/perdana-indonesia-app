from django.urls import include, path

urlpatterns = [
    path('regions/', include(('region.urls', 'region'), namespace='region')),
]
