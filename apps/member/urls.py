from django.urls import path
from apps.member import viewsets
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=True)
router.register('members', viewsets.ArcherMemberViewset, basename='member')
router.register('regionals', viewsets.RegionalViewSet, basename='regional')
router.register('provinces', viewsets.ProvinceViewSet, basename='province')
router.register('branchs', viewsets.BranchViewSet, basename='branch')
router.register('clubs', viewsets.ClubViewSet, basename='club')
router.register('units', viewsets.UnitViewSet, basename='unit')
router.register('archery-ranges', viewsets.ArcheryRangeViewSet, basename='archery-range')
router.register('profile', viewsets.UserProfileViewSet, basename='profile')

urlpatterns = [
    path('login', viewsets.LoginViewset.as_view(), name='login'),
    path('register', viewsets.RegisterViewset.as_view({'post': 'create'}), name='register'),
]

urlpatterns += router.urls
