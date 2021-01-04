from django.urls import include, path

urlpatterns = [
    path('dashboard/', include(('dashboardd.api.urls', 'dashboard_api'), namespace='dashboard_api')),
    path('archer/', include(('archer.api.urls', 'archer_api'), namespace='archer_api')),
]
