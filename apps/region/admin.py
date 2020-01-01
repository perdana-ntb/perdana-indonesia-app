from django.contrib import admin

from orm.models import region

# Register your models here.


# @admin.register(region.Region)
# class RegionModelAdmin(admin.ModelAdmin):
#     list_display = ['name']


@admin.register(region.Province)
class ProvinceModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'regional']
