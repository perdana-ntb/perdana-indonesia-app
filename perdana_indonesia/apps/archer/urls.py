from django.urls import path

from .views import ArcherLoginFormView, ArcherRegistrationFormView

urlpatterns = [
    path('registration', ArcherRegistrationFormView.as_view(), name='registration'),
    path('login', ArcherLoginFormView.as_view(), name='login'),
]
