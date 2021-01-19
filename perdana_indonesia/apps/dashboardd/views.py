from typing import Any, Dict, List

from archer.models import Archer
from core.choices import GENDER_CHOICES
from core.permissions import (PERDANA_CLUB_MANAGEMENT_USER_ROLE,
                              PERDANA_MANAGEMENT_USER_ROLE, PERDANA_USER_ROLE)
from core.views import RoleBasesAccessTemplateView, RoleBasesAccessView
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.shortcuts import redirect
from django.urls.base import reverse


class DashboardRouterView(RoleBasesAccessView):
    allowed_roles = PERDANA_USER_ROLE

    def mappedDashboardRedirectedUrl(self) -> Dict:
        defaultKwargs = {'province_code': self.archer.region_code_name}
        return {
            PERDANA_MANAGEMENT_USER_ROLE[0]: reverse('dashboardd:puslat', kwargs=defaultKwargs),
            PERDANA_MANAGEMENT_USER_ROLE[1]: reverse('dashboardd:puslat', kwargs=defaultKwargs),
            PERDANA_MANAGEMENT_USER_ROLE[2]: reverse('dashboardd:puslat', kwargs=defaultKwargs),
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

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['archerTotal'] = self.getArcherQuerySet().count()
        context['applicantTotal'] = self.archerQuerySet.filter(
            approval_status__verified=False).count()
        context['archerByGenderPieChartData'] = self.getArcherByGenderPieChartData()
        context['mappedArcherByDistrictTableData'] = self.getMappedArcherByDistrictTableData()
        return context
