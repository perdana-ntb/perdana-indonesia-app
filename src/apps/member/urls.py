from django.urls import path
from rest_framework.routers import DefaultRouter

from . import viewsets

router = DefaultRouter(trailing_slash=True)
router.register('members', viewsets.ArcherMemberViewset, basename='member')
router.register('regionals', viewsets.RegionalViewSet, basename='regional')
router.register('provinces', viewsets.ProvinceViewSet, basename='province')
router.register('branchs', viewsets.BranchViewSet, basename='branch')
router.register('clubunitss', viewsets.ClubUnitViewSet, basename='clubunit')
router.register('profile', viewsets.UserProfileViewSet, basename='profile')

urlpatterns = [
    path('login', viewsets.LoginViewset.as_view(), name='login'),
    path('register', viewsets.RegisterViewset.as_view({'post': 'create'}), name='register'),
]

urlpatterns += router.urls
