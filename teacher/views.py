from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum
from nur_comp.models import ListTeacher, ListStudent, Group
from .models import Journal, Schedule, Homework

def is_teacher(user):
    return hasattr(user, 'listteacher')

def is_student(user):
    return hasattr(user, 'liststudent')

def login_portal(request):
    return render(request, 'registration/portal.html')

def dashboard_redirect(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_dashboard')
        if is_teacher(request.user):
            return redirect('teacher_dashboard')
        if is_student(request.user):
            return redirect('student_dashboard')
    return redirect('login')

@login_required
@user_passes_test(is_teacher)
def teacher_dashboard(request):
    teacher = request.user.listteacher
    my_groups = Group.objects.filter(teacher=teacher)
    total_students = ListStudent.objects.filter(group__in=my_groups).count()
    total_points = Journal.objects.filter(teacher=teacher).aggregate(Sum('points'))['points__sum'] or 0
    return render(request, 'teacher/dashboard.html', {
        'teacher': teacher, 'groups': my_groups, 'total_students': total_students,
        'total_points': total_points, 'page_title': 'Мугалимдин панели'
    })

@login_required
@user_passes_test(is_teacher)
def teacher_groups(request):
    teacher = request.user.listteacher
    groups = Group.objects.filter(teacher=teacher)
    return render(request, 'teacher/groups.html', {'groups': groups, 'teacher': teacher})

# МЫНА УШУЛ ФУНКЦИЯНЫ КОШТУК:
@login_required
@user_passes_test(is_teacher)
def group_journal(request, group_id):
    teacher = request.user.listteacher
    group = get_object_or_404(Group, id=group_id, teacher=teacher)
    students = ListStudent.objects.filter(group=group)
    return render(request, 'teacher/journal.html', {
        'group': group, 'students': students, 'teacher': teacher, 'page_title': 'Журнал'
    })

@login_required
@user_passes_test(is_teacher)
def teacher_schedule(request):
    teacher = request.user.listteacher
    schedule = Schedule.objects.filter(teacher=teacher).order_by('day_of_week')
    return render(request, 'teacher/schedule.html', {'schedule': schedule, 'teacher': teacher})

@login_required
@user_passes_test(is_teacher)
def teacher_homework(request):
    teacher = request.user.listteacher
    my_groups = Group.objects.filter(teacher=teacher)
    homeworks = Homework.objects.filter(group__in=my_groups).order_by('-created_at')
    return render(request, 'teacher/homework.html', {'homeworks': homeworks, 'teacher': teacher})