from typing import Any, Dict

from archer.models import Archer
from core.permissions import PERDANA_MANAGEMENT_USER_ROLE, PERDANA_USER_ROLE
from core.views import RoleBasesAccessFormView, RoleBasesAccessListView
from django.contrib import messages
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.urls.base import reverse
from django.views import View
from region.models import Kabupaten, Kelurahan

from club.forms import ClubForm

from .models import Club


class RegionalClubJsonView(View):
    def getVillageOrNone(self, regionId):
        try:
            return Kelurahan.objects.get(pk=regionId)
        except Kelurahan.DoesNotExist:
            return None

    def get(self, request, **kwargs):
        village = self.getVillageOrNone(kwargs.get('region_id'))
        if village:
            queryset = Club.objects.filter(
                province_code=village.kecamatan.kabupaten.provinsi.code
            ).values('id', 'name')
        else:
            queryset = []
        return JsonResponse(data=list(queryset), safe=False)


class ClubListView(RoleBasesAccessListView):
    allowed_roles = PERDANA_MANAGEMENT_USER_ROLE
    template_name = 'organisation/club_list.html'
    queryset = Club.objects.all()
    context_object_name = 'clubs'

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.archer: Archer = None

    def mappedClubGoupQueryset(self, queryset: QuerySet):
        city: Kabupaten = self.archer.kelurahan.kecamatan.kabupaten
        return {
            PERDANA_USER_ROLE[0]: queryset,
            PERDANA_USER_ROLE[1]: queryset.filter(province_code=city.provinsi.code),
            PERDANA_USER_ROLE[2]: queryset.filter(city_code=city.code),
            PERDANA_USER_ROLE[3]: queryset.filter(pk=self.archer.club.pk)
        }

    def mappedClubGoupTableTitleDisplayed(self):
        kabupaten: Kabupaten = self.archer.kelurahan.kecamatan.kabupaten
        return {
            PERDANA_USER_ROLE[0]: 'Semua Pusat Latihan dalam Regional',
            PERDANA_USER_ROLE[1]: 'Semua Pusat Latihan di %s' % kabupaten.provinsi.name,
            PERDANA_USER_ROLE[2]: 'Semua Pusat Latihan di %s' % kabupaten.name,
            PERDANA_USER_ROLE[3]: 'Semua Pusat Latihan %s' % self.archer.club.name
        }

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title_header'] = self.mappedClubGoupTableTitleDisplayed()[self.archer.role]
        context['displayAddButton'] = self.archer.role in PERDANA_MANAGEMENT_USER_ROLE[1:2]
        context['kabupatens'] = Kabupaten.objects.filter(
            provinsi=self.archer.kelurahan.kecamatan.kabupaten.provinsi
        )
        return context

    def get_queryset(self) -> QuerySet:
        self.archer = self.request.user.archer
        return self.mappedClubGoupQueryset(super().get_queryset())[self.archer.role]


class ClubAddFormView(RoleBasesAccessFormView):
    allowed_roles = PERDANA_MANAGEMENT_USER_ROLE[1:2]
    template_name = 'organisation/club_add.html'
    form_class = ClubForm

    def get_success_url(self) -> str:
        return reverse('club:clubs', kwargs=self.kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['kabupatens'] = Kabupaten.objects.filter(
            provinsi=self.request.user.archer.kelurahan.kecamatan.kabupaten.provinsi
        )
        return context

    def form_valid(self, form: ClubForm) -> HttpResponse:
        form.save()
        messages.success(
            self.request, 'Pusat Latihan %s berhasil di tambahkan' % form.cleaned_data.get('name'),
            extra_tags='success'
        )
        return redirect(self.get_success_url())
