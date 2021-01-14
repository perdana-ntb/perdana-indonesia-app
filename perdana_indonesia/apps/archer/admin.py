from core.admin import DefaultAdminMixin
from django.contrib import admin

from .models import Archer, ArcherApprovalDocument, ArcherApprovalStatus


@admin.register(Archer)
class ArcherModelAdmin(DefaultAdminMixin, admin.ModelAdmin):
    pass


@admin.register(ArcherApprovalStatus)
class ArcherApprovalStatusModelAdmin(DefaultAdminMixin, admin.ModelAdmin):
    pass


@admin.register(ArcherApprovalDocument)
class ArcherApprovalDocumentModelAdmin(DefaultAdminMixin, admin.ModelAdmin):
    pass
