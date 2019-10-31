from django.urls import path

from . import views

urlpatterns = [
    path('', views.UnitListView.as_view(), name='list'),
    path('add', views.UnitAddFormView.as_view(), name='add'),
    path('<int:pk>/edit', views.UnitEditFormView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.UnitDeleteView.as_view(), name='delete'),
    path('<int:pk>/detail/', views.UnitDetailView.as_view(), name='detail'),
]
