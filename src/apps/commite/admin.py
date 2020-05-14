from django.contrib import admin

from commite.models import (ClubUnitCommiteMember, PengcabCommiteMember,
                                 PengprovCommiteMember, RegionalCommiteMember)


class BaseCommiteModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'sk_number', 'position', 'periode', 'address', 'phone', 'gender']
    search_fields = ['user', 'sk_number', 'phone']
    list_filter = ['gender']

# Register your models here.
@admin.register(RegionalCommiteMember)
class RegionalCommiteMemberModelAdmin(BaseCommiteModelAdmin):
    def get_list_display(self, request):
        display = super().get_list_display(request)
        display.append('regional')
        return display


@admin.register(PengprovCommiteMember)
class PengprovCommiteMemberModelAdmin(BaseCommiteModelAdmin):
    def get_list_display(self, request):
        display = super().get_list_display(request)
        display.append('province')
        return display


@admin.register(PengcabCommiteMember)
class PengcabCommiteMemberModelAdmin(BaseCommiteModelAdmin):
    def get_list_display(self, request):
        display = super().get_list_display(request)
        display.append('branch')
        return display


@admin.register(ClubUnitCommiteMember)
class ClubUnitCommiteMemberModelAdmin(BaseCommiteModelAdmin):
    pass


# @admin.register(UnitCommiteMember)
# class UnitCommiteMemberModelAdmin(BaseCommiteModelAdmin):
#     pass
