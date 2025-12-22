from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('groups/', views.teacher_groups, name='teacher_groups'), # Бул жер ката берип жаткан
    path('journal/<int:group_id>/', views.group_journal, name='group_journal'),
    path('schedule/', views.teacher_schedule, name='teacher_schedule'),
    path('homework/', views.teacher_homework, name='teacher_homework'),
]