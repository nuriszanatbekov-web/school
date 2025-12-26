from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum  # Упайларды тез эсептөө үчүн
from nur_comp.models import ListStudent, Group
# Эгер Journal жана Schedule моделдериңиз teacher тиркемесинде болсо:
from teacher.models import Journal, Schedule


def is_student(user):
    return hasattr(user, 'liststudent')


@login_required
@user_passes_test(is_student, login_url='login')
def student_dashboard(request):
    student = request.user.liststudent
    # Окуучунун бааларын алуу
    my_grades = Journal.objects.filter(student=student).order_by('-date')
    group = student.group

    # Упайларды эсептөө (эгер баалар жок болсо 0 чыгат)
    total_points = my_grades.aggregate(Sum('points'))['points__sum'] or 0

    context = {
        'student': student,
        'group': group,
        'my_grades': my_grades[:5],  # Акыркы 5 бааны гана көрсөтүү үчүн
        'total_points': total_points,
        'page_title': 'Окуучунун жеке кабинети'
    }
    return render(request, 'student/dashboard.html', context)


@login_required
@user_passes_test(is_student, login_url='login')
def student_schedule(request):
    student = request.user.liststudent
    # Окуучунун группасына тиешелүү графикти алуу
    schedule = Schedule.objects.filter(group=student.group).order_by('day_of_week')

    context = {
        'schedule': schedule,
        'student': student,
        'page_title': 'Менин сабак графигим'
    }
    return render(request, 'student/schedule.html', context)


@login_required
@user_passes_test(is_student, login_url='login')
def student_homework(request):
    """Сиздин катаңызды чечүүчү жаңы функция"""
    student = request.user.liststudent
    # Бул жерге үй тапшырмаларды алуу логикасын кошсоңуз болот
    context = {
        'student': student,
        'page_title': 'Үй тапшырмалар'
    }
    return render(request, 'student/homework.html', context)