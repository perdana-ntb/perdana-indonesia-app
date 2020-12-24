from django.http import JsonResponse
from django.views import View
from region.models import Kelurahan

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
            ).values('id', 'name', 'org_type')
        else:
            queryset = []
        return JsonResponse(data=list(queryset), safe=False)
