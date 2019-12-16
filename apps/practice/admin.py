from django.contrib import admin

from orm import practice

# Register your models here.


@admin.register(practice.TargetType)
class TargetTypeModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


@admin.register(practice.Practice)
class PracticeModelAdmin(admin.ModelAdmin):
    list_display = ['member', 'target_type', 'distance', 'series', 'arrow', 'status', 'signed']
    search_fields = ['member', 'target_type', 'distance']


@admin.register(practice.PracticeSeries)
class PracticeSeriesModelAdmin(admin.ModelAdmin):
    list_display = ['practice', 'photo', 'closed']


@admin.register(practice.PracticeScore)
class PracticeScoreModelAdmin(admin.ModelAdmin):
    list_display = ['serie', 'score']
