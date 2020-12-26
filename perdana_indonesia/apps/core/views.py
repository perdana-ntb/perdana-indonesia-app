from typing import Any

from archer.models import Archer
from django import http
from django.conf import settings
from django.contrib.auth.mixins import (AccessMixin, LoginRequiredMixin,
                                        UserPassesTestMixin)
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.urls.base import reverse
from django.views.generic import DetailView, FormView, ListView, TemplateView
from django.views.generic.base import View

from core.permissions import PERDANA_ARCHER_USER_ROLE


class UserAuthenticatedRedirectMixin(AccessMixin):
    def dispatch(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            archer = request.user.archer
            userGroup = archer.user.groups.first()
            if userGroup.name in PERDANA_ARCHER_USER_ROLE:
                return redirect('archer:profile', archer.region_code_name)
            else:
                return redirect('dashboardd:main', archer.region_code_name)
        return super().dispatch(request, *args, **kwargs)


class ProfileCompleteRequiredMixin(AccessMixin):
    force_update_profile_groups = PERDANA_ARCHER_USER_ROLE

    def dispatch(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        userGroup = request.user.groups.first()
        if '/archer/complete-profile' not in request.path and \
                userGroup.name in self.force_update_profile_groups:
            archer: Archer = request.user.archer
            if not archer.isProfileComplete:
                return redirect('archer:complete-profile', archer.region_code_name)
        return super().dispatch(request, *args, **kwargs)


class LoginRequiredView(LoginRequiredMixin, ProfileCompleteRequiredMixin, View):
    login_url = settings.LOGIN_URL


class LoginRequiredTemplateView(LoginRequiredMixin, ProfileCompleteRequiredMixin, TemplateView):
    login_url = settings.LOGIN_URL


class LoginRequiredListView(LoginRequiredMixin, ProfileCompleteRequiredMixin, ListView):
    login_url = settings.LOGIN_URL


class LoginRequiredFormView(LoginRequiredMixin, ProfileCompleteRequiredMixin, FormView):
    login_url = settings.LOGIN_URL


class LoginRequiredDetailView(LoginRequiredMixin, ProfileCompleteRequiredMixin, DetailView):
    login_url = settings.LOGIN_URL


class BaseRoleAccessMixin(UserPassesTestMixin):
    allowed_groups = ()

    def test_func(self):
        user = self.request.user
        try:
            return bool(
                user.is_authenticated
                and user.archer.approved
                and list(user.groups.values_list('name', flat=True))[0] in self.allowed_groups
                and user.archer.region_code_name == self.kwargs.get('province_code')
            )
        except (IndexError, AttributeError) as e:
            print(str(e))
            return False

    def getArcher(self):
        return self.request.user.archer


class RoleBasesAccessView(BaseRoleAccessMixin, LoginRequiredView):
    pass


class RoleBasesAccessTemplateView(BaseRoleAccessMixin, LoginRequiredTemplateView):
    pass


class RoleBasesAccessFormView(BaseRoleAccessMixin, LoginRequiredFormView):
    pass


class RoleBasesAccessListView(BaseRoleAccessMixin, LoginRequiredListView):
    pass


class RoleBasesAccessDetailView(BaseRoleAccessMixin, LoginRequiredDetailView):
    pass


class AutoRedirectView(View):
    def get(self, request, **kwargs):
        return redirect('archer:login', 'indonesia')
