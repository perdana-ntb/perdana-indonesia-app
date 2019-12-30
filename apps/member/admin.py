from django.contrib import admin
from orm.models import member
# Register your models here.


@admin.register(member.ArcherMember)
class ArcherMemberModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'phone', 'club', 'gender', 'approved']
    search_fields = ['user', 'phone']
    list_filter = ['gender', 'approved']


@admin.register(member.Periode)
class PeriodeModelAdmin(admin.ModelAdmin):
    list_display = ['time_periode']
