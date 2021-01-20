from typing import Any, Dict

from core.permissions import (PERDANA_ARCHER_USER_ROLE,
                              PERDANA_CLUB_MANAGEMENT_USER_ROLE,
                              PERDANA_MANAGEMENT_USER_ROLE, PERDANA_USER_ROLE)
from core.utils.generator import generate_qrcode_from_text
from core.views import (RoleBasesAccessDetailView, RoleBasesAccessFormView,
                        RoleBasesAccessListView, RoleBasesAccessTemplateView,
                        RoleBasesAccessView, UserAuthenticatedRedirectMixin)
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
from django.utils import timezone
from django.views.generic import FormView
from django.views.generic.base import View
from region.models import Kabupaten, Provinsi

from .forms import (ArcherCompleteDocumentForm, ArcherLoginForm,
                    ArcherRegistrationForm)
from .models import Archer, ArcherApprovalDocument, ArcherApprovalStatus


class ArcherRegistrationFormView(FormView):
    template_name = 'archer/registration.html'
    form_class = ArcherRegistrationForm
    success_url = 'archer:registration'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['provinces'] = Provinsi.objects.all()
        return ctx

    @transaction.atomic
    def form_valid(self, form: ArcherRegistrationForm):
        user = User.objects.create_user(
            username=form.cleaned_data.pop('username'),
            password=form.cleaned_data.pop('password'),
        )

        publicPhoto = form.cleaned_data.pop('public_photo')
        identityCardPhoto = form.cleaned_data.pop('identity_card_photo')
        archer: Archer = Archer.objects.create(user=user, **form.cleaned_data)

        approvalDocument: ArcherApprovalDocument = archer.approval_document
        approvalDocument.public_photo = publicPhoto
        approvalDocument.identity_card_photo = identityCardPhoto
        approvalDocument.save()

        messages.success(
            self.request, 'Pendaftaran sebagai anggota Perdana Indonesia berhasil. '
            'Silahkan Login menggunakan username dan password yang telah anda buat',
            extra_tags='success'
        )
        return redirect(self.success_url, **self.kwargs)

    def form_invalid(self, form: ArcherRegistrationForm):
        for error in form.errors.values():
            messages.error(self.request, error, extra_tags='danger')
        return super().form_invalid(form)


class ArcherLoginFormView(UserAuthenticatedRedirectMixin, FormView):
    template_name = 'archer/login.html'
    form_class = ArcherLoginForm
    success_url = 'dashboardd:router'

    def form_valid(self, form):
        credentials = form.cleaned_data
        user: User = authenticate(request=self.request, **credentials)
        if user:
            archer: Archer = user.archer
            login(self.request, user)
            if archer.role in PERDANA_ARCHER_USER_ROLE:
                self.success_url = 'archer:profile'
            return redirect(self.success_url, province_code=archer.region_code_name)
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
    allowed_roles = PERDANA_USER_ROLE
    template_name = 'archer/archer_profile.html'


class ArcherProfileDetailView(RoleBasesAccessDetailView):
    allowed_roles = PERDANA_MANAGEMENT_USER_ROLE
    template_name = 'archer/archer_profile_detail.html'
    context_object_name = 'archer'
    queryset = Archer.objects.all()

    def mappedQuerySet(self):
        archer: Archer = self.request.user.archer
        kabupaten = archer.kelurahan.kecamatan.kabupaten
        return{
            PERDANA_MANAGEMENT_USER_ROLE[0]: self.queryset.all(),
            PERDANA_MANAGEMENT_USER_ROLE[1]: self.queryset.filter(
                region_code_name=archer.region_code_name
            ),
            PERDANA_MANAGEMENT_USER_ROLE[2]: self.queryset.filter(
                club__city_code=kabupaten.code
            ),
            PERDANA_MANAGEMENT_USER_ROLE[3]: self.queryset.filter(club=archer.club),
        }

    def get_queryset(self) -> QuerySet:
        return self.mappedQuerySet()[self.request.user.archer.role]


class ArcherCompleteDocumentFormView(RoleBasesAccessFormView):
    allowed_roles = PERDANA_USER_ROLE
    template_name = 'archer/archer_complete_document.html'
    form_class = ArcherCompleteDocumentForm

    def get_success_url(self) -> str:
        return reverse('archer:profile', kwargs=self.kwargs)

    def form_valid(self, form: Form) -> HttpResponse:
        approvalDocument: ArcherApprovalDocument = self.request.user.archer.approval_document
        approvalDocument.skck = form.cleaned_data.get('skck')
        approvalDocument.latsar_certificate = form.cleaned_data.get('latsar_certificate')
        if not approvalDocument.isDocumentComplete:
            approvalDocument.save()

        messages.success(
            self.request, 'Dokumen pendaftaran berhasil diperbarui',
            extra_tags='success'
        )
        return super().form_valid(form)


class ArcherClubMemberListView(RoleBasesAccessListView):
    allowed_roles = PERDANA_MANAGEMENT_USER_ROLE
    template_name = 'archer/archer_member_list.html'
    queryset = Archer.objects.filter(approval_status__verified=True)
    context_object_name = 'archers'

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
        context['title_header'] = self.mappedUserGoupTableTitleDisplayed()[self.archer.role]
        return context

    def get_queryset(self) -> QuerySet:
        return self.mappedUserGoupQueryset(super().get_queryset())[self.archer.role]


class ArcherClubApplicantListView(RoleBasesAccessListView):
    allowed_roles = PERDANA_MANAGEMENT_USER_ROLE
    template_name = 'archer/archer_applicant_list.html'
    queryset = Archer.objects.filter(approval_status__verified=False)
    context_object_name = 'archers'

    def mappedUserGoupQueryset(self, queryset: QuerySet):
        city: Kabupaten = self.archer.kelurahan.kecamatan.kabupaten
        return {
            PERDANA_USER_ROLE[1]: queryset.filter(region_code_name=self.archer.region_code_name),
            PERDANA_USER_ROLE[2]: queryset.filter(club__city_code=city.code),
            PERDANA_USER_ROLE[3]: queryset.filter(club=self.archer.club)
        }

    def mappedUserGoupTableTitleDisplayed(self):
        return {
            PERDANA_USER_ROLE[1]: 'Anggota Belum Terverifikasi',
            PERDANA_USER_ROLE[2]: 'Anggota Belum Terverifikasi',
            PERDANA_USER_ROLE[3]: 'Semua pendaftar Puslat %s' % self.archer.club.name
        }

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title_header'] = self.mappedUserGoupTableTitleDisplayed()[self.archer.role]
        return context

    def get_queryset(self) -> QuerySet:
        return self.mappedUserGoupQueryset(super().get_queryset())[self.archer.role]


class GenerateArcherQRCodeView(RoleBasesAccessView):
    allowed_roles = PERDANA_CLUB_MANAGEMENT_USER_ROLE

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
    allowed_roles = PERDANA_MANAGEMENT_USER_ROLE

    def getArcherObject(self, pk) -> Archer:
        try:
            return Archer.objects.get(pk=pk)
        except Archer.DoesNotExist:
            raise Http404

    def verifyAccessArcherData(self, pk) -> bool:
        instance: Archer = self.getArcherObject(pk)
        if self.archer.role == PERDANA_MANAGEMENT_USER_ROLE[3]:
            return instance.club.pk == self.archer.club.pk
        elif self.archer.role == PERDANA_MANAGEMENT_USER_ROLE[2]:
            return bool(
                instance.club.city_code == self.archer.club.city_code
            )
        elif self.archer.role == PERDANA_MANAGEMENT_USER_ROLE[1]:
            return bool(
                instance.region_code_name ==
                self.archer.region_code_name
            )
        return False

    def updateApprovalData(self, pk: int, requestData: dict) -> ArcherApprovalDocument:
        instance: Archer = self.getArcherObject(pk)
        appStatus: ArcherApprovalStatus = instance.approval_status
        if self.archer.role == PERDANA_MANAGEMENT_USER_ROLE[3]:
            appStatus.puslat_approved = True
            appStatus.puslat_approved_by = self.archer.user
            appStatus.puslat_approved_on = timezone.now()
            messages.success(
                self.request,
                'Berhasil verifikasi data anggota atas nama %s' % instance.full_name,
                extra_tags='success'
            )
        elif self.archer.role == PERDANA_MANAGEMENT_USER_ROLE[2]:
            if appStatus.puslat_approved:
                appStatus.dpc_approved = True
                appStatus.dpc_approved_by = self.archer.user
                appStatus.dpc_approved_on = timezone.now()
                messages.success(
                    self.request,
                    'Berhasil verifikasi data anggota atas nama %s' % instance.full_name,
                    extra_tags='success'
                )
            else:
                messages.error(
                    self.request, 'Gagal verifikasi data anggota atas nama %s, '
                    'Puslat belum melakukan verifikasi data' % instance.full_name,
                    extra_tags='danger'
                )
        elif self.archer.role == PERDANA_MANAGEMENT_USER_ROLE[1]:
            if appStatus.dpc_approved:
                appStatus.dpd_approved = True
                appStatus.dpd_approved_by = self.archer.user
                appStatus.dpd_approved_on = timezone.now()

                user: User = instance.user
                user.username = requestData.get('membership_number')
                user.save()
                # Trigger signal to recreate QRCode
                instance.save()

                messages.success(
                    self.request,
                    'Berhasil verifikasi data anggota atas nama %s' % instance.full_name,
                    extra_tags='success'
                )
            else:
                messages.error(
                    self.request, 'Gagal verifikasi data anggota atas nama %s, '
                    'DPC belum melakukan verifikasi data' % instance.full_name,
                    extra_tags='danger'
                )
        appStatus.save()
        return appStatus

    @transaction.atomic
    def post(self, request, **kwargs):
        instance = self.getArcherObject(self.kwargs.get('pk'))
        hasAccess = self.verifyAccessArcherData(instance.pk)
        if hasAccess:
            self.updateApprovalData(instance.pk, request.POST)
            return redirect(
                'archer:profile-detail',
                province_code=instance.region_code_name,
                pk=instance.pk
            )
        raise Http404('Tidak dapat mengakses data ini')


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
