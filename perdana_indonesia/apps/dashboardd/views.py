from typing import Any, Dict, List

from archer.models import Archer
from club.models import ArcheryRange, Club
from core.choices import GENDER_CHOICES
from core.permissions import (PERDANA_CLUB_MANAGEMENT_USER_ROLE,
                              PERDANA_MANAGEMENT_USER_ROLE, PERDANA_USER_ROLE)
from core.views import RoleBasesAccessTemplateView, RoleBasesAccessView
from django.db.models.aggregates import Count
from django.db.models.expressions import F
from django.db.models.query import QuerySet
from django.shortcuts import redirect
from django.urls.base import reverse
from region.models import Kabupaten


class DashboardRouterView(RoleBasesAccessView):
    allowed_roles = PERDANA_USER_ROLE

    def mappedDashboardRedirectedUrl(self) -> Dict:
        defaultKwargs = {'province_code': self.archer.region_code_name}
        return {
            PERDANA_MANAGEMENT_USER_ROLE[0]: reverse('dashboardd:puslat', kwargs=defaultKwargs),
            PERDANA_MANAGEMENT_USER_ROLE[1]: reverse('dashboardd:puslat', kwargs=defaultKwargs),
            PERDANA_MANAGEMENT_USER_ROLE[2]: reverse('dashboardd:pengcab', kwargs=defaultKwargs),
            PERDANA_MANAGEMENT_USER_ROLE[3]: reverse('dashboardd:puslat', kwargs=defaultKwargs)
        }

    def get(self, request, **kwargs):
        return redirect(self.mappedDashboardRedirectedUrl()[self.archer.role])


class DashboardPuslatTemplateView(RoleBasesAccessTemplateView):
    template_name = 'dashboardd/dashboard_puslat_manager.html'
    allowed_roles = PERDANA_CLUB_MANAGEMENT_USER_ROLE
    archerQuerySet = Archer.objects.all()

    def getArcherQuerySet(self) -> QuerySet:
        return self.archerQuerySet.filter(
            approval_status__verified=True, club=self.archer.club
        )

    def getArcherByGenderPieChartData(self) -> Dict:
        return {
            'title': 'Total anggota berdasarkan jenis kelamin',
            'datasets': [
                {'name': gender[0], 'y':self.getArcherQuerySet().filter(gender=gender[0]).count()}
                for gender in GENDER_CHOICES
            ]
        }

    def getMappedArcherByDistrictTableData(self) -> List:
        return self.getArcherQuerySet().values('kelurahan__kecamatan__name')\
            .annotate(by_kecamatan_total=Count('kelurahan__kecamatan'))\
            .values('kelurahan__kecamatan__name', 'by_kecamatan_total')\
            .order_by('-by_kecamatan_total')

    def getMappedArcherByDistrictPieChartData(self) -> Dict:
        dataSets = self.getArcherQuerySet().values('kelurahan__kecamatan__name')\
            .annotate(name=F('kelurahan__kecamatan__name'), y=Count('kelurahan__kecamatan'))\
            .values('name', 'y').order_by('-y')
        return {
            'title': 'Sebaran Anggota Berdasarkan Kecamatan',
            'datasets': list(dataSets)
        }

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['archerTotal'] = self.getArcherQuerySet().count()
        context['applicantTotal'] = self.archerQuerySet.filter(
            approval_status__verified=False).count()
        context['archerByGenderPieChartData'] = self.getArcherByGenderPieChartData()
        context['mappedArcherByDistrictPieChartData'] = self.getMappedArcherByDistrictPieChartData()
        context['mappedArcherByDistrictTableData'] = self.getMappedArcherByDistrictTableData()
        print(context)
        return context


class DashboardPengcabTemplateView(RoleBasesAccessTemplateView):
    template_name = 'dashboardd/dashboard_pengcab.html'
    allowed_roles = (PERDANA_USER_ROLE[2], )
    archerQuerySet = Archer.objects.all()

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.kabupaten: Kabupaten = None

    def getArcherQuerySet(self) -> QuerySet:
        return self.archerQuerySet.filter(
            approval_status__verified=True,
            club__city_code=self.kabupaten.code
        )

    def getArcherByGenderPieChartData(self) -> Dict:
        return {
            'title': 'Total anggota berdasarkan jenis kelamin',
            'datasets': [
                {'name': gender[0], 'y':self.getArcherQuerySet().filter(gender=gender[0]).count()}
                for gender in GENDER_CHOICES
            ]
        }

    def getMappedArcherByDistrictTableData(self) -> List:
        return self.getArcherQuerySet().values('kelurahan__kecamatan__name')\
            .annotate(by_kecamatan_total=Count('kelurahan__kecamatan'))\
            .values('kelurahan__kecamatan__name', 'by_kecamatan_total')\
            .order_by('-by_kecamatan_total')

    def getMappedArcherByDistrictPieChartData(self) -> Dict:
        dataSets = self.getArcherQuerySet().values('kelurahan__kecamatan__name')\
            .annotate(name=F('kelurahan__kecamatan__name'), y=Count('kelurahan__kecamatan'))\
            .values('name', 'y')\
            .order_by('-y')
        return {
            'title': 'Sebaran Anggota Berdasarkan Kecamatan',
            'datasets': list(dataSets)
        }

    def getMappedPuslatByDistrictTableData(self) -> List:
        return Club.objects.filter(city_code=self.kabupaten.code)\
            .values('village__kecamatan__name')\
            .annotate(by_kecamatan_total=Count('village__kecamatan'))\
            .values('village__kecamatan__name', 'by_kecamatan_total')\
            .order_by('-by_kecamatan_total')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        self.kabupaten = self.archer.kelurahan.kecamatan.kabupaten

        context['archerTotal'] = self.getArcherQuerySet().count()
        context['applicantTotal'] = self.archerQuerySet.filter(
            approval_status__verified=False).count()
        context['puslatTotal'] = Club.objects.filter(
            city_code=self.kabupaten.code
        ).count()
        context['archeryRangeTotal'] = ArcheryRange.objects.filter(
            managed_by__city_code=self.kabupaten.code
        ).count()
        context['archerByGenderPieChartData'] = self.getArcherByGenderPieChartData()
        context['mappedArcherByDistrictPieChartData'] = self.getMappedArcherByDistrictPieChartData()
        context['mappedArcherByDistrictTableData'] = self.getMappedArcherByDistrictTableData()
        context['mappedPuslatByDistrictTableData'] = self.getMappedPuslatByDistrictTableData()
        return context
