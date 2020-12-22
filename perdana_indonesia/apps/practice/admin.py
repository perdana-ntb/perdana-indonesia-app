from core.admin import DefaultAdminMixin
from django.contrib import admin

from practice.models import (PracticeContainer, PracticeScore, PracticeSeries,
                             TargetType)


@admin.register(TargetType)
class TargetTypeModelAdmin(DefaultAdminMixin, admin.ModelAdmin):
    pass


class PracticeSeriesTabularInline(admin.TabularInline):
    model = PracticeSeries


@admin.register(PracticeContainer)
class PracticeContainerModelAdmin(DefaultAdminMixin, admin.ModelAdmin):
    inlines = (PracticeSeriesTabularInline, )


@admin.register(PracticeSeries)
class PracticeSeriesModelAdmin(DefaultAdminMixin, admin.ModelAdmin):
    pass


@admin.register(PracticeScore)
class PracticeScoreModelAdmin(DefaultAdminMixin, admin.ModelAdmin):
    pass
