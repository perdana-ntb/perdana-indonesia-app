from core.permissions import PERDANA_ARCHER_USER_ROLE, PERDANA_USER_ROLE
from core.views import RoleBasesAccessTemplateView
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.generic import FormView
from django.views.generic.base import View
from region.models import Provinsi

from .forms import ArcherLoginForm, ArcherRegistrationForm
from .models import Archer


class ArcherRegistrationFormView(FormView):
    template_name = 'archer/registration.html'
    form_class = ArcherRegistrationForm
    success_url = 'archer:registration'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['provinces'] = Provinsi.objects.all()
        return ctx

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Pendaftaran sebagai anggota Perdana Indonesia berhasil. '
                         'Data anda akan di verifikasi terlebih dahulu '
                         'oleh pengurus klub/satuan tempat mendaftar',
                         extra_tags='success')
        return redirect(self.success_url, **self.kwargs)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class ArcherLoginFormView(FormView):
    template_name = 'archer/login.html'
    form_class = ArcherLoginForm
    success_url = 'dashboardd:main'

    def form_valid(self, form):
        credentials = form.cleaned_data
        user: User = authenticate(request=self.request, **credentials)
        if user:
            archer: Archer = user.archer
            if archer.approved:
                # if archer.is_profile_complete():
                login(self.request, user)
                if list(user.groups.values_list('name', flat=True))[0] in PERDANA_ARCHER_USER_ROLE:
                    self.success_url = 'archer:profile'
                return redirect(self.success_url, province_code=archer.region_code_name)
            messages.error(
                self.request, 'Akun anda belum diverifikasi oleh pengurus',
                extra_tags='danger'
            )
        else:
            messages.error(
                self.request, 'Username / No. anggota atau password salah',
                extra_tags='danger'
            )
        return redirect('archer:login', **self.kwargs)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class ArcherLogoutView(View):
    def get(self, request, **kwargs):
        if self.request.user.is_authenticated:
            logout(request=self.request)
        return redirect(settings.LOGIN_URL)


class ArcherUserProfileTemplateView(RoleBasesAccessTemplateView):
    template_name = 'archer/archer_profile.html'
    allowed_groups = PERDANA_USER_ROLE
