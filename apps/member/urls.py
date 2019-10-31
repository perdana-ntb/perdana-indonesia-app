from django.urls import path

from . import views

urlpatterns = [
    path('', views.MemberListView.as_view(), name='list'),
    path('add', views.MemberAddFormView.as_view(), name='add'),
    path('<int:pk>/detail', views.MemberDetailView.as_view(), name='detail'),
    path('<int:pk>/edit', views.MemberEditFormView.as_view(), name='edit'),
    path('<int:pk>/delete', views.MemberDeleteView.as_view(), name='delete'),
]
