from typing import Any, Dict

from core.permissions import (PERDANA_ARCHER_USER_ROLE,
                              PERDANA_CLUB_MANAGEMENT_USER_ROLE,
                              PERDANA_MANAGEMENT_USER_ROLE, PERDANA_USER_ROLE)
from core.utils.generator import generate_qrcode_from_text
from core.views import (RoleBasesAccessFormView, RoleBasesAccessListView,
                        RoleBasesAccessTemplateView, RoleBasesAccessView,
                        UserAuthenticatedRedirectMixin)
from django import http
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models.query import QuerySet
from django.forms.forms import Form
from django.http.response import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import FormView
from django.views.generic.base import View
from region.models import Kabupaten, Provinsi

from .forms import (ArcherCompleteProfileForm, ArcherLoginForm,
                    ArcherRegistrationForm)
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


class ArcherLoginFormView(UserAuthenticatedRedirectMixin, FormView):
    template_name = 'archer/login.html'
    form_class = ArcherLoginForm
    success_url = 'dashboardd:main'

    def form_valid(self, form):
        credentials = form.cleaned_data
        user: User = authenticate(request=self.request, **credentials)
        if user:
            archer: Archer = user.archer
            if archer.approved:
                login(self.request, user)
                userGroup = user.groups.first()
                if userGroup.name in PERDANA_ARCHER_USER_ROLE:
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
    allowed_groups = PERDANA_USER_ROLE
    template_name = 'archer/archer_profile.html'


class ArcherCompleteProfileFormView(RoleBasesAccessFormView):
    allowed_groups = PERDANA_USER_ROLE
    template_name = 'archer/archer_complete_profile.html'
    form_class = ArcherCompleteProfileForm

    def dispatch(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        instance: Archer = request.user.archer
        if instance.isProfileComplete:
            return redirect(reverse('archer:profile', kwargs=self.kwargs))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse('archer:profile', kwargs=self.kwargs)

    def form_valid(self, form: Form) -> HttpResponse:
        instance: Archer = self.getArcher()
        instance.skck = form.cleaned_data.get('skck')
        instance.photo = form.cleaned_data.get('photo')
        instance.public_photo = form.cleaned_data.get('public_photo')
        instance.body_weight = form.cleaned_data.get('body_weight')
        instance.body_height = form.cleaned_data.get('body_height')
        instance.draw_length = form.cleaned_data.get('draw_length')
        instance.save()
        messages.success(self.request, 'Data profile berhasil di perbarui', extra_tags='success')
        return redirect(self.get_success_url())


class ArcherClubMemberListView(RoleBasesAccessListView):
    allowed_groups = PERDANA_MANAGEMENT_USER_ROLE
    template_name = 'archer/archer_member_list.html'
    queryset = Archer.objects.filter(user__isnull=False)
    context_object_name = 'archers'

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.archer = None
        self.userGroup = None

    def mappedUserGoupQueryset(self, queryset: QuerySet):
        city: Kabupaten = self.archer.kelurahan.kecamatan.kabupaten
        return {
            PERDANA_USER_ROLE[0]: queryset,
            PERDANA_USER_ROLE[1]: queryset.filter(region_code_name=self.archer.region_code_name),
            PERDANA_USER_ROLE[2]: queryset.filter(club__city_code=city.code),
            PERDANA_USER_ROLE[3]: queryset.filter(club=self.archer.club)
        }

    def mappedUserGoupTableTitleDisplayed(self):
        return {
            PERDANA_USER_ROLE[0]: 'Semua anggota dalam Regional',
            PERDANA_USER_ROLE[1]: 'Semua anggota dalam Provinsi',
            PERDANA_USER_ROLE[2]: 'Semua anggota dalam Cabang (Kabupaten)',
            PERDANA_USER_ROLE[3]: 'Semua anggota %s' % self.archer.club.name
        }

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['tableTitle'] = self.mappedUserGoupTableTitleDisplayed()[self.userGroup.name]
        return context

    def get_queryset(self) -> QuerySet:
        self.archer = self.request.user.archer
        self.userGroup = self.archer.getUserGroup()
        return self.mappedUserGoupQueryset(super().get_queryset())[self.userGroup.name]


class ArcherClubApplicantListView(RoleBasesAccessListView):
    allowed_groups = PERDANA_MANAGEMENT_USER_ROLE
    template_name = 'archer/archer_applicant_list.html'
    queryset = Archer.objects.filter(user__isnull=True)
    context_object_name = 'archers'

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.archer = None
        self.userGroup = None

    def mappedUserGoupQueryset(self, queryset: QuerySet):
        city: Kabupaten = self.archer.kelurahan.kecamatan.kabupaten
        return {
            PERDANA_USER_ROLE[0]: queryset,
            PERDANA_USER_ROLE[1]: queryset.filter(region_code_name=self.archer.region_code_name),
            PERDANA_USER_ROLE[2]: queryset.filter(club__city_code=city.code),
            PERDANA_USER_ROLE[3]: queryset.filter(club=self.archer.club)
        }

    def mappedUserGoupTableTitleDisplayed(self):
        return {
            PERDANA_USER_ROLE[0]: 'Semua pendaftar dalam Regional',
            PERDANA_USER_ROLE[1]: 'Semua pendaftar dalam Provinsi',
            PERDANA_USER_ROLE[2]: 'Semua pendaftar dalam Cabang (Kabupaten)',
            PERDANA_USER_ROLE[3]: 'Semua pendaftar %s' % self.archer.club.name
        }

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['tableTitle'] = self.mappedUserGoupTableTitleDisplayed()[self.userGroup.name]
        return context

    def get_queryset(self) -> QuerySet:
        self.archer = self.request.user.archer
        self.userGroup = self.archer.getUserGroup()
        return self.mappedUserGoupQueryset(super().get_queryset())[self.userGroup.name]


class GenerateArcherQRCodeView(RoleBasesAccessView):
    allowed_groups = PERDANA_CLUB_MANAGEMENT_USER_ROLE

    def getArcherObject(self, archerId) -> Archer:
        try:
            return Archer.objects.get(pk=archerId)
        except Archer.DoesNotExist:
            raise http.Http404

    def get(self, request, **kwargs):
        instance = self.getArcherObject(kwargs.get('archer_id'))
        instance.qrcode = generate_qrcode_from_text(instance.user.username)
        instance.save()
        messages.success(
            request, 'Berhasil generate QRCode untuk Archer %s' % instance.user.username,
            extra_tags='success'
        )
        return redirect('archer:club-members', province_code=instance.region_code_name)


class ArcherMembershipApprovalFormView(RoleBasesAccessView):
    allowed_groups = PERDANA_CLUB_MANAGEMENT_USER_ROLE
    success_url = 'archer:club-members'

    def getArcherObject(self, pk) -> Archer:
        try:
            return Archer.objects.get(pk=pk)
        except Archer.DoesNotExist:
            raise Http404

    @transaction.atomic
    def post(self, request, **kwargs):
        instance = self.getArcherObject(self.kwargs.get('pk'))
        if not instance.approved:
            try:
                user = User.objects.get(username=request.POST.get('membership_number'))
                messages.success(request, 'No. Anggota %s sudah diberikan kepada anggota lain'
                                 % request.POST.get('membership_number'), extra_tags='danger')
                self.success_url = 'archer:club-applicants'
            except User.DoesNotExist:
                user = User.objects.create(username=request.POST.get('membership_number'))
                user.set_password('membership_number')
                user.save()

                instance.user = user
                instance.qrcode = generate_qrcode_from_text(instance.user.username)
                instance.approved = True
                instance.approved_by = request.user
                instance.save()
                messages.success(request, 'Pendaftar %s telah diterima sebagai anggota'
                                 % instance.full_name, extra_tags='success')

        return redirect(self.success_url, instance.region_code_name)


class ArcherMembershipCheckView(View):
    template_name = 'archer/archer_membership_check.html'

    def getArcherObjectOrNone(self, archerId) -> Archer:
        if archerId:
            try:
                return Archer.objects.get(user__username=archerId)
            except Archer.DoesNotExist:
                return None
        return None

    def get(self, request, **kwargs):
        instance = self.getArcherObjectOrNone(request.GET.get('archer_id'))
        return render(request, self.template_name, context={
            'instance': instance,
        })
