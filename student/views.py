from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
# Негизги моделдер nur_comp тиркемесинде жайгашкан:
from nur_comp.models import ListStudent, Group
# Журнал жана График teacher тиркемесинде жайгашкан:
from teacher.models import Journal, Schedule

def is_student(user):
    return hasattr(user, 'liststudent')

@login_required
@user_passes_test(is_student)
def student_dashboard(request):
    student = request.user.liststudent
    my_grades = Journal.objects.filter(student=student).order_by('-date')
    group = student.group
    total_points = sum(grade.points for grade in my_grades)

    context = {
        'student': student,
        'group': group,
        'my_grades': my_grades,
        'total_points': total_points,
        'page_title': 'Окуучунун жеке кабинети'
    }
    return render(request, 'student/dashboard.html', context)

@login_required
@user_passes_test(is_student)
def student_schedule(request):
    student = request.user.liststudent
    schedule = Schedule.objects.filter(group=student.group).order_by('day_of_week')

    context = {
        'schedule': schedule,
        'student': student,
        'page_title': 'Менин сабак графигим'
    }
    return render(request, 'student/schedule.html', context)