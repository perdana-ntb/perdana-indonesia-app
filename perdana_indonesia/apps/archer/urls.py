from django.urls import path

from .views import (ArcherClubApplicantListView, ArcherClubMemberListView,
                    ArcherCompleteProfileFormView, ArcherLoginFormView,
                    ArcherLogoutView, ArcherMembershipApprovalFormView,
                    ArcherMembershipCheckView, ArcherRegistrationFormView,
                    ArcherUserProfileTemplateView, GenerateArcherQRCodeView)

urlpatterns = [
    path('registration', ArcherRegistrationFormView.as_view(), name='registration'),
    path('login', ArcherLoginFormView.as_view(), name='login'),
    path('logout', ArcherLogoutView.as_view(), name='logout'),
    path('membership-check', ArcherMembershipCheckView.as_view(), name='membership-check'),
    path('profile', ArcherUserProfileTemplateView.as_view(), name='profile'),
    path('complete-profile', ArcherCompleteProfileFormView.as_view(), name='complete-profile'),
    path('club-members', ArcherClubMemberListView.as_view(), name='club-members'),
    path('club-applicants', ArcherClubApplicantListView.as_view(), name='club-applicants'),
    path('generate-qrcode/<int:archer_id>', GenerateArcherQRCodeView.as_view(), name='gen-qrcode'),
    path('approve/<int:pk>', ArcherMembershipApprovalFormView.as_view(), name='approve'),
]
