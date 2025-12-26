from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum
from nur_comp.models import ListTeacher, ListStudent, Group
from .models import Journal, Schedule, Homework
import datetime

def is_teacher(user):
    return hasattr(user, 'listteacher')

def is_student(user):
    return hasattr(user, 'liststudent')

def login_portal(request):
    return render(request, 'registration/portal.html')


def dashboard_redirect(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.is_superuser:
        return redirect('dashboard')

    # Окуучуну текшерүү (related_name 'liststudent' экенин тактаңыз)
    if hasattr(request.user, 'liststudent'):
        return redirect('student_dashboard')

    # Мугалимди текшерүү (related_name 'listteacher' экенин тактаңыз)
    if hasattr(request.user, 'listteacher'):
        return redirect('teacher_dashboard')

    return redirect('portal')

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
def teacher_groups(request):
    try:
        # Учурдагы кирген колдонуучунун мугалимдик профилин табабыз
        teacher_profile = request.user.listteacher
        # Ушул мугалимге гана тиешелүү группаларды алабыз
        groups = Group.objects.filter(teacher=teacher_profile)
    except:
        groups = []

    return render(request, 'teacher/groups.html', {'groups': groups})
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
def teacher_schedule(request):
    try:
        teacher = request.user.listteacher
    except AttributeError:
        return render(request, 'errors/404.html', {'message': 'Мугалим профили табылган жок'})

    # МЫНА УШУЛ ЖЕРГЕ КОШОСУЗ:
    # -------------------------------------------------------
    time_slots = []
    for hour in range(9, 20):
        time_slots.append(datetime.time(hour, 0))
        time_slots.append(datetime.time(hour, 30))
    # -------------------------------------------------------

    # Калган код өзгөрүүсүз калат:
    days = [1, 2, 3, 4, 5, 6]  # Дүйшөмбүдөн Ишембиге чейин
    schedule_items = Schedule.objects.filter(teacher=teacher).select_related('group')

    full_schedule = {}
    for item in schedule_items:
        # Саатты мүнөтү менен кошо ачкыч катары колдонобуз
        time_key = item.start_time.replace(second=0, microsecond=0)
        full_schedule[(time_key, item.day_of_week)] = item

    context = {
        'teacher': teacher,
        'time_slots': time_slots,
        'days': days,
        'full_schedule': full_schedule,
        'page_title': 'Менин сабак графигим'
    }

    return render(request, 'teacher/schedule.html', context)


@login_required
@user_passes_test(is_teacher)
def teacher_students(request):
    teacher = request.user.listteacher
    # Мугалимдин бардык группаларын алабыз
    my_groups = Group.objects.filter(teacher=teacher)
    # Ошол группаларга тиешелүү окуучуларды табабыз
    students = ListStudent.objects.filter(group__in=my_groups).select_related('group')

    return render(request, 'teacher/students_list.html', {
        'students': students,
        'page_title': 'Менин окуучуларым'
    })

@login_required
@user_passes_test(is_teacher)
def teacher_homework(request):
    teacher = request.user.listteacher
    my_groups = Group.objects.filter(teacher=teacher)
    homeworks = Homework.objects.filter(group__in=my_groups).order_by('-created_at')
    return render(request, 'teacher/homework.html', {'homeworks': homeworks, 'teacher': teacher})