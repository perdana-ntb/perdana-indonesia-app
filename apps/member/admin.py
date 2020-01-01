from django.contrib import admin
from orm.models import member
from core.utils.generator import generate_qrcode_from_text
# Register your models here.

def approve_archer_member(modeladmin, request, queryset):
    for instance in queryset:
        instance.approved = True
        instance.approved_by = request.user
        instance.qrcode = generate_qrcode_from_text(instance.user.username)
        instance.save()


approve_archer_member.short_description = "Approve Or Regenerate QRCode"

@admin.register(member.ArcherMember)
class ArcherMemberModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'phone', 'club', 'gender', 'approved']
    search_fields = ['user', 'phone']
    list_filter = ['gender', 'approved']
    actions = [approve_archer_member, ]
    


@admin.register(member.Periode)
class PeriodeModelAdmin(admin.ModelAdmin):
    list_display = ['time_periode']
