from core.admin import DefaultAdminMixin
from django.contrib import admin

from region.models import Kabupaten, Kecamatan, Kelurahan, Provinsi, Regional


@admin.register(Regional)
class RegionalModelAdmin(DefaultAdminMixin, admin.ModelAdmin):
    pass


@admin.register(Provinsi)
class ProvinsiModelAdmin(DefaultAdminMixin, admin.ModelAdmin):
    pass


@admin.register(Kabupaten)
class KabupatenModelAdmin(DefaultAdminMixin, admin.ModelAdmin):
    pass


@admin.register(Kecamatan)
class KecamatanModelAdmin(DefaultAdminMixin, admin.ModelAdmin):
    pass


@admin.register(Kelurahan)
class KelurahanModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'kecamatan', 'kabupaten', 'provinsi')
    search_fields = ('name', 'kecamatan__name', 'kecamatan__kabupaten__name')
    list_filter = ('kecamatan__name', )

    def kecamatan(self, obj):
        return obj.kecamatan.name

    def kabupaten(self, obj):
        return obj.kecamatan.kabupaten.name

    def provinsi(self, obj):
        return obj.kecamatan.kabupaten.provinsi.name
