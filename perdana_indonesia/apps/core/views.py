from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (DetailView, FormView, ListView, TemplateView,
                                  View)


class LoginRequiredView(LoginRequiredMixin, View):
    login_url = settings.LOGIN_URL


class LoginRequiredTemplateView(LoginRequiredMixin, TemplateView):
    login_url = settings.LOGIN_URL


class LoginRequiredListView(LoginRequiredMixin, ListView):
    login_url = settings.LOGIN_URL


class LoginRequiredFormView(LoginRequiredMixin, FormView):
    login_url = settings.LOGIN_URL


class LoginRequiredDetailView(LoginRequiredMixin, DetailView):
    login_url = settings.LOGIN_URL


class BaseRoleAccessMixin(UserPassesTestMixin):
    allowed_groups = ()

    def test_func(self):
        user = self.request.user
        print()
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

    def get_archer(self):
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
