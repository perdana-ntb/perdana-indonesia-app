from django.contrib import admin

from core.admin import DefaultAdminMixin
from menu.models import AppMenu, MenuCategory


@admin.register(MenuCategory)
class AppMenuCategoryModelAdmin(DefaultAdminMixin, admin.ModelAdmin):
    pass


@admin.register(AppMenu)
class AppMenuModelAdmin(DefaultAdminMixin, admin.ModelAdmin):
    pass
