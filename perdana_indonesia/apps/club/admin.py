from core.admin import DefaultAdminMixin
from django.contrib import admin

from club.models import ArcheryRange, Club

# Register your models here.


@admin.register(Club)
class ClubModelAdmin(DefaultAdminMixin, admin.ModelAdmin):
    pass


@admin.register(ArcheryRange)
class ArcheryRangeModelAdmin(DefaultAdminMixin, admin.ModelAdmin):
    pass
