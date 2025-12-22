from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('schedule/', views.student_schedule, name='student_schedule'),
]