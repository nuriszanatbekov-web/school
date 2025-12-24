from django.contrib import admin
from .models import Journal, Schedule, Homework

@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    # Тизмеде көрүнө турган талаалар
    list_display = ('date', 'student', 'teacher', 'group', 'entry_type', 'points')
    # Оң жактагы фильтрлер
    list_filter = ('entry_type', 'group', 'teacher', 'date')
    # Издөө талаалары (Окуучунун аты же мугалимдин ФИОсу боюнча)
    search_fields = ('student__full_name', 'teacher__fio')
    # Дата боюнча иерархия (Senior стилинде)
    date_hierarchy = 'date'

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('get_day_display', 'start_time', 'end_time', 'teacher', 'group', 'room')
    list_filter = ('day_of_week', 'teacher', 'group')
    search_fields = ('teacher__fio', 'group__name', 'room')
    ordering = ('day_of_week', 'start_time')

    # Апта күндөрүнүн атын тизмеде көрсөтүү үчүн функция
    def get_day_display(self, obj):
        return dict(obj.DAYS).get(obj.day_of_week)
    get_day_display.short_description = 'Апта күнү'

@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    # Моделиңизде 'teacher' жана 'deadline' жок болгондуктан, аларды алып салдык
    list_display = ('title', 'group', 'created_at')
    list_filter = ('group', 'created_at')
    search_fields = ('title', 'description')