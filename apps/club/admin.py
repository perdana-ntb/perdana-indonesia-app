from django.contrib import admin
from orm.models import club
# Register your models here.


@admin.register(club.Club)
class ClubModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'address']


@admin.register(club.Unit)
class UnitModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'address']
