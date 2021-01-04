from archer.api.viewsets import (ArhcerCheckMembershipViewSet,
                                 ArhcerProfileViewSet, LoginViewSet)
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register('login', LoginViewSet, basename='login')
router.register('profile', ArhcerProfileViewSet, basename='profile')
router.register(
    'check-membership', ArhcerCheckMembershipViewSet, basename='check-membership'
)

urlpatterns = []
urlpatterns += router.urls
