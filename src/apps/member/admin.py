from django.contrib import admin

from core.utils.generator import generate_qrcode_from_text
from member.models import ArcherMember, ChangeRequest, PhysicInformation


@admin.register(ArcherMember)
class ArcherMemberModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'phone', 'clubunit', 'gender', 'approved']
    search_fields = ['user', 'phone']
    list_filter = ['gender', 'approved']
    actions = ['approve_archer_member', ]

    def approve_archer_member(self, request, queryset):
        for instance in queryset:
            instance.approved = True
            instance.approved_by = request.user
            instance.qrcode = generate_qrcode_from_text(instance.user.username)
            instance.save()

    approve_archer_short_description = "Approve Or Regenerate QRCode"


@admin.register(PhysicInformation)
class PhysicInformationModelAdmin(admin.ModelAdmin):
    list_display = ['basemember']


@admin.register(ChangeRequest)
class ChangeRequestModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'reason', 'status', 'closed']
