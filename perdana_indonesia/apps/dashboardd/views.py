from typing import Any, Dict, List

from archer.models import Archer
from core.choices import GENDER_CHOICES
from core.permissions import PERDANA_MANAGEMENT_USER_ROLE
from core.views import RoleBasesAccessTemplateView
from django.contrib.auth.models import Group
from django.db.models.query import QuerySet
from region.models import Kabupaten


class DashboardTemplateView(RoleBasesAccessTemplateView):
    template_name = 'dashboardd/dashboard.html'
    allowed_groups = PERDANA_MANAGEMENT_USER_ROLE
    queryset = Archer.objects.filter(user__isnull=False)

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.archer: Archer = None
        self.userGroup: Group = None

    def mappedUserGoupQueryset(self) -> QuerySet:
        city: Kabupaten = self.archer.kelurahan.kecamatan.kabupaten
        return {
            PERDANA_MANAGEMENT_USER_ROLE[0]: self.queryset,
            PERDANA_MANAGEMENT_USER_ROLE[1]: self.queryset.filter(
                region_code_name=self.archer. region_code_name
            ),
            PERDANA_MANAGEMENT_USER_ROLE[2]: self.queryset.filter(
                club__city_code=city.code
            ),
            PERDANA_MANAGEMENT_USER_ROLE[3]: self.queryset.filter(
                club=self.archer.club
            )
        }

    def mappedDisplayTitle(self) -> QuerySet:
        return {
            PERDANA_MANAGEMENT_USER_ROLE[0]: 'Dashboard Regional',
            PERDANA_MANAGEMENT_USER_ROLE[1]: 'Dashboard Pengurus Provinsi',
            PERDANA_MANAGEMENT_USER_ROLE[2]: 'Dashboard Pengurus Cabang',
            PERDANA_MANAGEMENT_USER_ROLE[3]: 'Dashboard Pengurus Club / Satuan'
        }

    def getArcherInformation(self) -> List:
        queryset = self.mappedUserGoupQueryset()[self.userGroup.name]
        return [
            {
                'title': 'Total Anggota Aktif',
                'value': queryset.filter(is_active=True).count(),
                'options': {
                    'bg_class': 'bg-primary'
                }
            },
            {
                'title': 'Total Anggota Tidak Aktif',
                'value': queryset.filter(is_active=False).count(),
                'options': {
                    'bg_class': 'bg-primary'
                }
            },
            {
                'title': 'Total Anggota Pria',
                'value': queryset.filter(gender=GENDER_CHOICES[0][0]).count(),
                'options': {
                    'bg_class': 'bg-warning'
                }
            },
            {
                'title': 'Total Anggota Wanita',
                'value': queryset.filter(gender=GENDER_CHOICES[1][0]).count(),
                'options': {
                    'bg_class': 'bg-danger'
                }
            },
        ]

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        self.archer = self.getArcher()
        self.userGroup = self.archer.user.groups.first()

        context['archers_mapping_information'] = self.getArcherInformation()
        context['title_header'] = self.mappedDisplayTitle()[self.userGroup.name]
        return context
