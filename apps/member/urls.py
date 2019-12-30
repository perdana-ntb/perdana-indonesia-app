from django.urls import path
from apps.member import viewsets
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=True)
router.register('members', viewsets.ArcherMemberViewset, base_name='member')
router.register('regionals', viewsets.RegionalViewSet, base_name='regional')
router.register('provinces', viewsets.ProvinceViewSet, base_name='province')
router.register('branchs', viewsets.BranchViewSet, base_name='branch')
router.register('clubs', viewsets.ClubViewSet, base_name='club')
router.register('units', viewsets.UnitViewSet, base_name='unit')

urlpatterns = [
    path('login', viewsets.LoginViewset.as_view(), name='login'),
    path('register', viewsets.RegisterViewset.as_view({'post': 'create'}), name='register'),
    path('profile', viewsets.UserProfileViewSet.as_view({'get': 'retrieve'}), name='profile'),
]

urlpatterns += router.urls
