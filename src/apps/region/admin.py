from django.contrib import admin

from region.models import Province

# Register your models here.


# @admin.register(region.Region)
# class RegionModelAdmin(admin.ModelAdmin):
#     list_display = ['name']


@admin.register(Province)
class ProvinceModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'regional']
