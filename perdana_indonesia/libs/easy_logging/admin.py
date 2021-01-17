from core.admin import DefaultAdminMixin
from django.contrib import admin

from .models import EasyLogging


@admin.register(EasyLogging)
class EasyLogginModelAdmin(DefaultAdminMixin, admin.ModelAdmin):
    list_filter = ('method', )
