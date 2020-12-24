from core.admin import DefaultAdminMixin
from django.contrib import admin

from .models import Archer


@admin.register(Archer)
class ArcherModelAdmin(DefaultAdminMixin, admin.ModelAdmin):
    pass
