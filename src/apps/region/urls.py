from django.urls import path

from . import views

urlpatterns = [
    path('', views.RegionFormView.as_view(), name='view'),
]
