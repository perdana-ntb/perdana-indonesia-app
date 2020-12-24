from django.urls import path

from .views import (ArcherLoginFormView, ArcherLogoutView,
                    ArcherRegistrationFormView, ArcherUserProfileTemplateView)

urlpatterns = [
    path('registration', ArcherRegistrationFormView.as_view(), name='registration'),
    path('login', ArcherLoginFormView.as_view(), name='login'),
    path('logout', ArcherLogoutView.as_view(), name='logout'),
    path('profile', ArcherUserProfileTemplateView.as_view(), name='profile'),
]
