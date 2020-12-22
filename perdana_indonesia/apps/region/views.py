from django.http import JsonResponse
from django.views.generic import View

from region.models import Kabupaten, Kecamatan, Kelurahan, Provinsi


class ProvinsiJsonView(View):
    def get(self, request, **kwargs):
        queryset = Provinsi.objects.values('id', 'code', 'name', 'code_name')
        return JsonResponse(data=list(queryset), safe=False)


class KabupatenJsonView(View):
    def get(self, request, **kwargs):
        queryset = Kabupaten.objects.filter(provinsi__code=kwargs.get('parent_code'))\
            .values('id', 'code', 'name')
        return JsonResponse(data=list(queryset), safe=False)


class KecamatanJsonView(View):
    def get(self, request, **kwargs):
        queryset = Kecamatan.objects.filter(kabupaten__code=kwargs.get('parent_code'))\
            .values('id', 'code', 'name')
        return JsonResponse(data=list(queryset), safe=False)


class KelurahanJsonView(View):
    def get(self, request, **kwargs):
        queryset = Kelurahan.objects.filter(kecamatan__code=kwargs.get('parent_code'))\
            .values('id', 'code', 'name')
        return JsonResponse(data=list(queryset), safe=False)
