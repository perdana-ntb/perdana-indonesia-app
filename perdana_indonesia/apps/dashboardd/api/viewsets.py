from typing import Any, Dict, List

from archer.models import Archer
from core.choices import GENDER_CHOICES
from core.permissions import PERDANA_USER_ROLE, IsGeneralUser
from django.contrib.auth.models import Group
from region.models import Kabupaten
from rest_framework import views
from rest_framework.response import Response


class DashboardViewSet(views.APIView):
    permission_classes = (IsGeneralUser, )

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.arhcerQueryset = Archer.objects.filter(user__isnull=False)
        self.archer: Archer = None
        self.userGroup: Group = None

    def mappedUserGoupArcherQueryset(self) -> Dict:
        city: Kabupaten = self.archer.kelurahan.kecamatan.kabupaten
        return {
            PERDANA_USER_ROLE[0]: self.arhcerQueryset,
            PERDANA_USER_ROLE[1]: self.arhcerQueryset,
            PERDANA_USER_ROLE[2]: self.arhcerQueryset.filter(
                region_code_name=self.archer. region_code_name
            ),
            PERDANA_USER_ROLE[3]: self.arhcerQueryset.filter(
                club__city_code=city.code
            ),
            PERDANA_USER_ROLE[4]: self.arhcerQueryset.filter(
                club=self.archer.club
            )
        }

    def mappedDisplayTitle(self) -> Dict:
        return {
            PERDANA_USER_ROLE[0]: 'Dashboard Personal',
            PERDANA_USER_ROLE[1]: 'Dashboard Regional',
            PERDANA_USER_ROLE[2]: 'Dashboard Pengurus Provinsi',
            PERDANA_USER_ROLE[3]: 'Dashboard Pengurus Cabang',
            PERDANA_USER_ROLE[4]: 'Dashboard Pengurus Club / Satuan'
        }

    def getBaseDashboardData(self) -> List:
        queryset = self.mappedUserGoupArcherQueryset()[self.userGroup.name]
        return [
            {
                'title': 'Total Anggota Aktif',
                'value': queryset.filter(is_active=True).count(),
                'type': 'text'
            },
            {
                'title': 'Total Anggota Tidak Aktif',
                'value': queryset.filter(is_active=False).count(),
                'type': 'text'
            },
            {
                'title': 'Total Anggota Pria',
                'value': queryset.filter(gender=GENDER_CHOICES[0][0]).count(),
                'type': 'text'
            },
            {
                'title': 'Total Anggota Wanita',
                'value': queryset.filter(gender=GENDER_CHOICES[1][0]).count(),
                'type': 'text'
            },
        ]

    def getPersonalDashboardData(self) -> List:
        return []

    def getRegionalDashboardData(self) -> List:
        dashboardData = self.getBaseDashboardData()
        dashboardData.extend([
            # Regional Data Here
        ])
        return dashboardData

    def getPengprovDashboardData(self) -> List:
        dashboardData = self.getBaseDashboardData()
        dashboardData.extend([
            # Pengprov Data Here
        ])
        return dashboardData

    def getPengcabDashboardData(self) -> List:
        dashboardData = self.getBaseDashboardData()
        dashboardData.extend([
            # Pengcab Data Here
        ])
        return dashboardData

    def getClubManagerDashboardData(self) -> List:
        dashboardData = self.getBaseDashboardData()
        dashboardData.extend([
            # Club Manager Data Here
        ])
        return dashboardData

    def mappedDashboardData(self) -> Dict:
        return {
            PERDANA_USER_ROLE[0]: self.getPersonalDashboardData(),
            PERDANA_USER_ROLE[1]: self.getRegionalDashboardData(),
            PERDANA_USER_ROLE[2]: self.getPengprovDashboardData(),
            PERDANA_USER_ROLE[3]: self.getPengcabDashboardData(),
            PERDANA_USER_ROLE[4]: self.getClubManagerDashboardData()
        }

    def get(self, request, *args, **kwargs):
        self.archer = request.user.archer
        self.userGroup = request.user.groups.first()

        return Response({
            'title': self.mappedDisplayTitle()[self.userGroup.name],
            'data': self.mappedDashboardData()[self.userGroup.name]
        })
