from django.contrib import admin
from .models import (
    ListTeacher, ListStudent, Group, Branch, Service,
    Category, Subject, AnalyticsReport
)

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('fio', 'email', 'phone_number', 'branch', 'tag')
    list_filter = ('branch', 'gender', 'tag')
    search_fields = ('fio', 'email', 'phone_number')
    filter_horizontal = ('subjects',)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'group', 'branch')
    list_filter = ('group', 'branch', 'gender')
    search_fields = ('full_name', 'email', 'phone_number')

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'teacher', 'start_date', 'is_active')

class AnalyticsReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    readonly_fields = ('created_at', 'data')

admin.site.register(ListTeacher, TeacherAdmin)
admin.site.register(ListStudent, StudentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(AnalyticsReport, AnalyticsReportAdmin)
admin.site.register(Branch)
admin.site.register(Service)
admin.site.register(Category)
admin.site.register(Subject)