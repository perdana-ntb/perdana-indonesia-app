from django.urls import path

from .views import (KabupatenJsonView, KecamatanJsonView, KelurahanJsonView,
                    ProvinsiJsonView)

urlpatterns = [
    path('provinces', ProvinsiJsonView.as_view(), name='provinces'),
    path('cities/<str:parent_code>', KabupatenJsonView.as_view(), name='cities'),
    path('districts/<str:parent_code>', KecamatanJsonView.as_view(), name='districts'),
    path('villages/<str:parent_code>', KelurahanJsonView.as_view(), name='villages'),
]
