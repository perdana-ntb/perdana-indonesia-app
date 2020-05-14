from django.contrib import admin

from club.models import ClubUnit

# Register your models here.


@admin.register(ClubUnit)
class ClubUnitModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'address']
