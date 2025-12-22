from django.shortcuts import render, redirect
from nur_comp.models import ListStudent, Group
from teacher.models import Journal, Schedule, Homework


def get_student_profile(request):
    """ Тест үчүн базадагы биринчи окуучуну алабыз (логинсиз кирүү үчүн) """
    return ListStudent.objects.first()


def student_dashboard(request):
    student = get_student_profile(request)
    # Окуучунун упайларынын тарыхы
    my_grades = Journal.objects.filter(student=student).order_by('-date')
    # Окуучунун группасы
    group = student.group

    context = {
        'student': student,
        'group': group,
        'my_grades': my_grades,
        'page_title': 'Окуучунун жеке кабинети'
    }
    return render(request, 'student/dashboard.html', context)


def student_schedule(request):
    student = get_student_profile(request)
    # Окуучунун группасына тиешелүү график
    schedule = Schedule.objects.filter(group=student.group).order_by('day_of_week')
    return render(request, 'student/schedule.html', {'schedule': schedule, 'student': student})