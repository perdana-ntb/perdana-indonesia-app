from typing import Any

from archer.models import Archer
from django import http
from django.conf import settings
from django.contrib.auth.mixins import (AccessMixin, LoginRequiredMixin,
                                        UserPassesTestMixin)
from django.http.response import Http404, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView, FormView, ListView, TemplateView
from django.views.generic.base import View

from core.permissions import PERDANA_ARCHER_USER_ROLE


class UserAuthenticatedRedirectMixin(AccessMixin):
    def dispatch(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            archer = request.user.archer
            if archer.role in PERDANA_ARCHER_USER_ROLE:
                return redirect('archer:profile', archer.region_code_name)
            else:
                return redirect('dashboardd:main', archer.region_code_name)
        return super().dispatch(request, *args, **kwargs)


class ProfileCompleteRequiredMixin(AccessMixin):
    force_update_profile_roles = PERDANA_ARCHER_USER_ROLE

    def dispatch(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        archer: Archer = request.user.archer
        allowedUrls = [
            reverse('archer:profile', kwargs={'province_code': archer.region_code_name}),
            reverse('archer:complete-document', kwargs={'province_code': archer.region_code_name}),
        ]
        if request.path not in allowedUrls and \
                archer.role in self.force_update_profile_roles:
            try:
                if not archer.approval_status.verified:
                    return redirect('archer:profile', archer.region_code_name)
            except (AttributeError, KeyError, ValueError):
                raise Http404('Request does not allowed')
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
    allowed_roles = ()

    def test_func(self):
        user = self.request.user
        try:
            return bool(
                user.is_authenticated and
                user.archer.role in self.allowed_roles and
                user.archer.region_code_name == self.kwargs.get('province_code')
            )
        except (IndexError, AttributeError):
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
