from django.urls import path

from . import views

urlpatterns = [
    path('', views.ClubListView.as_view(), name='list'),
    path('add', views.ClubAddFormView.as_view(), name='add'),
    path('<int:pk>/edit', views.ClubEditFormView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.CLubDeleteView.as_view(), name='delete'),
    path('<int:pk>/detail/', views.ClubDetailView.as_view(), name='detail'),
]
