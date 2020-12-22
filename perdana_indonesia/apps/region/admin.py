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
class KelurahanModelAdmin(DefaultAdminMixin, admin.ModelAdmin):
    pass
