from django.contrib import admin
from orm.models import commite


class BaseCommiteModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'sk_number', 'position', 'periode', 'address', 'phone', 'gender']
    search_fields = ['user', 'sk_number', 'phone']
    list_filter = ['gender']

# Register your models here.
@admin.register(commite.RegionalCommiteMember)
class RegionalCommiteMemberModelAdmin(BaseCommiteModelAdmin):
    def get_list_display(self, request):
        display = super().get_list_display(request)
        display.append('regional')
        return display


@admin.register(commite.PengprovCommiteMember)
class PengprovCommiteMemberModelAdmin(BaseCommiteModelAdmin):
    def get_list_display(self, request):
        display = super().get_list_display(request)
        display.append('province')
        return display


@admin.register(commite.PengcabCommiteMember)
class PengcabCommiteMemberModelAdmin(BaseCommiteModelAdmin):
    def get_list_display(self, request):
        display = super().get_list_display(request)
        display.append('branch')
        return display


@admin.register(commite.ClubCommiteMember)
class ClubCommiteMemberModelAdmin(BaseCommiteModelAdmin):
    pass


@admin.register(commite.UnitCommiteMember)
class UnitCommiteMemberModelAdmin(BaseCommiteModelAdmin):
    pass
