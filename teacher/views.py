from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Sum
from nur_comp.models import ListTeacher, ListStudent, Group
from .models import Journal, Schedule, Homework
import datetime


# --- БАГЫТТОО ЛОГИКАСЫ ---

def login_portal(request):
    """ Админ же Мугалим катары кирүүнү тандоо барагы """
    return render(request, 'registration/portal.html')


def dashboard_redirect(request):
    """ Ролго жараша багыттоо """
    if request.user.is_authenticated:
        teacher = getattr(request.user, 'listteacher', None)
        if teacher:
            return redirect('teacher_dashboard')
        if request.user.is_superuser:
            return redirect('dashboard')
    return redirect('portal')


# --- МУГАЛИМДИН КӨМӨКЧҮ ФУНКЦИЯСЫ ---

def get_teacher_profile(user):
    """ Мугалимдин профилин алуу (Логинсиз иштөө үчүн биринчи мугалимди кайтарат) """
    if user.is_authenticated and hasattr(user, 'listteacher'):
        return user.listteacher
    # Базада жок дегенде бир мугалим болушу керек
    return ListTeacher.objects.first()


# --- МУГАЛИМДИН НЕГИЗГИ ФУНКЦИЯЛАРЫ ---

def teacher_dashboard(request):
    """ Мугалимдин башкы панели """
    teacher = get_teacher_profile(request.user)
    if not teacher:
        messages.error(request, "Базада мугалимдер табылган жок!")
        return redirect('portal')

    my_groups = Group.objects.filter(teacher=teacher)
    total_students = ListStudent.objects.filter(group__in=my_groups).count()
    total_points = Journal.objects.filter(teacher=teacher).aggregate(Sum('points'))['points__sum'] or 0

    context = {
        'teacher': teacher,
        'groups': my_groups,
        'total_students': total_students,
        'total_points': total_points,
        'page_title': 'Менин Дашбордум'
    }
    return render(request, 'teacher/dashboard.html', context)


def teacher_groups(request):
    """ Мугалимдин группалары """
    teacher = get_teacher_profile(request.user)
    groups = Group.objects.filter(teacher=teacher)
    return render(request, 'teacher/groups.html', {
        'groups': groups,
        'page_title': 'Менин Группаларым'
    })


def group_journal(request, group_id):
    teacher = get_teacher_profile(request.user)  # Мугалимди алабыз
    group = get_object_or_404(Group, id=group_id, teacher=teacher)
    students = ListStudent.objects.filter(group=group)

    # ... калган логикаң ...

    return render(request, 'teacher/journal.html', {
        'group': group,
        'students': students,
        'teacher': teacher,  # БУЛ ЖЕРДИ СӨЗСҮЗ КОШ! (Үстүнкү жазуулар үчүн)
        'page_title': f"{group.name} - Журнал"
    })


def teacher_schedule(request):
    teacher = get_teacher_profile(request.user)
    schedule = Schedule.objects.filter(teacher=teacher)

    return render(request, 'teacher/schedule.html', {
        'schedule': schedule,
        'teacher': teacher,  # ЖАНА БУЛ ЖЕРДЕ ДАГЫ
        'page_title': 'Менин графигим'
    })

# --- ЖЕТИШПЕГЕН ФУНКЦИЯЛАР (КАТАНЫ ОҢДОО ҮЧҮН) ---

def teacher_schedule(request):
    teacher = get_teacher_profile(request.user)  # Мугалимди таап жатабыз
    schedule = Schedule.objects.filter(teacher=teacher)

    return render(request, 'teacher/schedule.html', {
        'schedule': schedule,
        'teacher': teacher,  # БУЛ САП СӨЗСҮЗ КЕРЕК! (Тексттер өзгөрүшү үчүн)
        'page_title': 'Сабактардын графиги'
    })


def teacher_homework(request):
    """ Үй тапшырмалар """
    teacher = get_teacher_profile(request.user)
    if not teacher:
        return redirect('portal')

    my_groups = Group.objects.filter(teacher=teacher)
    homeworks = Homework.objects.filter(group__in=my_groups).order_by('-created_at')

    return render(request, 'teacher/homework.html', {
        'homeworks': homeworks,
        'groups': my_groups,
        'page_title': 'Үй тапшырмалар'
    })