from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('schedule/', views.student_schedule, name='student_schedule'),
    # 'student_homework' шилтемесин сөзсүз кошуңуз, антпесе NoReverseMatch катасы чыга берет
    path('homework/', views.student_homework, name='student_homework'),
]