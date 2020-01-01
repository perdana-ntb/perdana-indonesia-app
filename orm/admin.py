from django.contrib import admin

from . import models

# Register your models here.


@admin.register(models.region.Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(models.club.Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'province']
