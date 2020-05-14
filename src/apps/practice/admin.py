from django.contrib import admin

from practice.models import (PracticeContainer, PracticeScore,
                                  PracticeSeries, TargetType)


@admin.register(TargetType)
class TargetTypeModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


@admin.register(PracticeContainer)
class PracticeModelAdmin(admin.ModelAdmin):
    list_display = ['member', 'target_type', 'distance', 'series', 'arrow', 'status', 'signed']
    search_fields = ['member', 'distance']


@admin.register(PracticeSeries)
class PracticeSeriesModelAdmin(admin.ModelAdmin):
    list_display = ['practice_container', 'photo', 'closed']


@admin.register(PracticeScore)
class PracticeScoreModelAdmin(admin.ModelAdmin):
    list_display = ['serie', 'score']
