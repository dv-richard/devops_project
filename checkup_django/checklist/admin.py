from django.contrib import admin
from .models import Section, TaskTemplate, Checklist, CheckItem

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('titre','ordre')
    list_editable = ('ordre',)

@admin.register(TaskTemplate)
class TaskTemplateAdmin(admin.ModelAdmin):
    list_display = ('nom','section','ordre')
    list_editable= ('section','ordre')

class CheckItemInline(admin.TabularInline):
    model = CheckItem
    extra = 1
    can_delete = True
    readonly_fields = ('nom',)

@admin.register(Checklist)
class ChecklistAdmin(admin.ModelAdmin):
    list_display = ('date','verifie_par')
    inlines = [CheckItemInline]
    ordering = ('-date',)
