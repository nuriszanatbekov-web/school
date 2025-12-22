from django.urls import reverse
from django.urls.exceptions import NoReverseMatch  # !!! NoReverseMatch импорттолду !!!

from rest_framework import viewsets, filters
from rest_framework.routers import DefaultRouter, APIRootView
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend

# --- МОДЕЛДЕР ЖАНА СЕРИАЛИЗЕРЛЕР ---
from .models import (
    ListStudent, ListTeacher, Group, Branch, Service,
    Category, Subject, AnalyticsReport
)
from django.shortcuts import render, get_object_or_404, redirect
from .forms import (
    StudentForm, TeacherForm, GroupForm, BranchForm,
    ServiceForm, CategoryForm, SubjectForm, AnalyticsReportForm
)

from .serializers import (
    # ===================================================
    # 1. ТОЛУК СЕРИАЛИЗЕРЛЕР (8)
    # ===================================================
    StudentSerializer, TeacherSerializer, GroupSerializer,
    BranchSerializer, ServiceSerializer, CategorySerializer,
    SubjectSerializer, AnalyticsReportSerializer,

    # ===================================================
    # 2. ТИЗМЕ СЕРИАЛИЗЕРЛЕР (8)
    # ===================================================
    TeacherListSerializer, StudentListSerializer, GroupListSerializer,
    BranchListSerializer, ServiceListSerializer, CategoryListSerializer,
    SubjectListSerializer, AnalyticsReportListSerializer
)


# ===================================================
# 1. CUSTOM ROUTER ЖАНА VIEWSET'ТЕР
# ===================================================

def get_config(model_name):
    configs = {
        'teachers': (ListTeacher, TeacherForm),
        'students': (ListStudent, StudentForm),
        'groups': (Group, GroupForm),
        'branches': (Branch, BranchForm),
        'services': (Service, ServiceForm),
        'categories': (Category, CategoryForm),
        'subjects': (Subject, SubjectForm),
        'analytics': (AnalyticsReport, AnalyticsReportForm),
    }
    return configs.get(model_name, (None, None))


# 2. Андан кийин гана аны колдонгон функцияларды жазыңыз
def add_item_view(request, model_name):
    ModelClass, FormClass = get_config(model_name)  # Эми бул жерде ката чыкпайт
    if not ModelClass:
        return redirect('dashboard')

    form = FormClass(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('list_view', model_name=model_name)

    return render(request, 'edit_template.html', {
        'form': form,
        'model_name': model_name,
        'page_title': 'Жаңы кошуу'
    })


def edit_item_view(request, model_name, item_id):
    ModelClass, FormClass = get_config(model_name)  # Бул жерде да иштейт
    item = get_object_or_404(ModelClass, id=item_id)

    form = FormClass(request.POST or None, request.FILES or None, instance=item)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('list_view', model_name=model_name)

    return render(request, 'edit_template.html', {
        'form': form,
        'model_name': model_name,
        'item': item,
        'page_title': 'Түзөтүү'
    })

def add_item_view(request, model_name):
    ModelClass, FormClass = get_config(model_name)
    if not ModelClass:
        return redirect('dashboard')

    if request.method == 'POST':
        form = FormClass(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_view', model_name=model_name)
    else:
        form = FormClass()

    return render(request, 'edit_template.html', {
        'form': form,
        'model_name': model_name,
        'page_title': 'Жаңы кошуу'
    })

def delete_item_view(request, model_name, item_id):
    model_map = {
        'teachers': ListTeacher,
        'students': ListStudent,
        'groups': Group,
        'branches': Branch,
        'categories': Category,
        'subjects': Subject,
        'services': Service,
        'analytics': AnalyticsReport,
    }

    if model_name in model_map:
        model_class = model_map[model_name]
        item = get_object_or_404(model_class, id=item_id)
        item.delete()  # Базадан өчүрүү

    return redirect('list_view', model_name=model_name)

def edit_item_view(request, model_name, item_id):
    # Моделдерди жана формаларды картага түшүрүү
    model_config = {
        'teachers': (ListTeacher, TeacherForm),
        'students': (ListStudent, StudentForm),
        'groups': (Group, GroupForm),
        'branches': (Branch, BranchForm),
        'services': (Service, ServiceForm),
        'categories': (Category, CategoryForm),
        'subjects': (Subject, SubjectForm),
        'analytics': (AnalyticsReport, AnalyticsReportForm),
    }

    if model_name not in model_config:
        return redirect('dashboard')

    ModelClass, FormClass = model_config[model_name]
    item = get_object_or_404(ModelClass, id=item_id)

    if request.method == 'POST':
        form = FormClass(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('list_view', model_name=model_name)
    else:
        form = FormClass(instance=item)

    return render(request, 'edit_template.html', {
        'form': form,
        'model_name': model_name,
        'item': item,
        'page_title': f"{model_name.capitalize()} түзөтүү"
    })

class CustomAPIRootView(APIRootView):
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CustomRouter(DefaultRouter):
    APIRootView = CustomAPIRootView


# Router'ду бул жерде инстанциялоо
router = CustomRouter()


# -----------------------------------------------------
# 2. VIEWSET'ТЕР
# -----------------------------------------------------

@extend_schema(tags=['Teachers'])
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = ListTeacher.objects.all().order_by('fio')
    serializer_class = TeacherSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['tag', 'branch']
    search_fields = ['fio', 'phone_number', 'email']

    def get_serializer_class(self):
        if self.action == 'list':
            return TeacherListSerializer
        return TeacherSerializer


@extend_schema(tags=['Students'])
class StudentViewSet(viewsets.ModelViewSet):
    queryset = ListStudent.objects.all().order_by('full_name')
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['group', 'branch']
    search_fields = ['full_name', 'phone_number', 'email']

    def get_serializer_class(self):
        if self.action == 'list':
            return StudentListSerializer
        return StudentSerializer


@extend_schema(tags=['Groups'])
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('-is_active', 'name')
    serializer_class = GroupSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active', 'subject', 'teacher']
    search_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return GroupListSerializer
        return GroupSerializer


@extend_schema(tags=['Branches'])
class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all().order_by('name')
    serializer_class = BranchSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'address', 'phone']

    def get_serializer_class(self):
        if self.action == 'list':
            return BranchListSerializer
        return BranchSerializer


@extend_schema(tags=['Categories'])
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return CategoryListSerializer
        return CategorySerializer


@extend_schema(tags=['Subjects'])
class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all().order_by('name')
    serializer_class = SubjectSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return SubjectListSerializer
        return SubjectSerializer


@extend_schema(tags=['Services'])
class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all().order_by('name')
    serializer_class = ServiceSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

    def get_serializer_class(self):
        if self.action == 'list':
            return ServiceListSerializer
        return ServiceSerializer


@extend_schema(tags=['Analytics'])
class AnalyticsReportViewSet(viewsets.ModelViewSet):
    queryset = AnalyticsReport.objects.all().order_by('-created_at')
    serializer_class = AnalyticsReportSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def get_serializer_class(self):
        if self.action == 'list':
            return AnalyticsReportListSerializer
        return AnalyticsReportSerializer


# -----------------------------------------------------
# 3. УНИВЕРСАЛДУУ ЛИСТ VIEW
# -----------------------------------------------------

# dashboard_view'ду list_view'га алмаштыруу
def list_view(request, model_name='dashboard'):
    """
    Универсалдуу View: Моделдин атына жараша тиешелүү шаблонду көрсөтөт.
    model_name='dashboard' болсо, башкы бетти көрсөтөт.
    """

    # API префикстерине моделдерди тууралоо
    model_map = {
        'teachers': ListTeacher,
        'students': ListStudent,
        'groups': Group,
        'branches': Branch,
        'categories': Category,
        'subjects': Subject,
        'services': Service,
        'analytics': AnalyticsReport,
        'dashboard': None  # Башкы бет үчүн
    }

    # Меню шилтемелерин дайыма түзүү
    menu_links = []
    prefixes = list(model_map.keys())[:-1]

    # Dashboard шилтемесин кошуу
    try:
        menu_links.append({'name': 'Dashboard', 'url': reverse('dashboard')})
    except NoReverseMatch:
        menu_links.append({'name': 'Dashboard', 'url': '/'})

    # Башка моделдерди кошуу
    for prefix in prefixes:
        display_name = prefix.replace('_', ' ').capitalize()

        # Шилтеме URL: /list/{prefix}/
        # 'list_view' URL атын колдонуу
        try:
            url_final = reverse('list_view', kwargs={'model_name': prefix})
        except NoReverseMatch:
            # Эгерде URL али туура каттала элек болсо, /api/ шилтемесин колдонуу
            url_final = f'{reverse("api-root")}{prefix}/'

        menu_links.append({
            'name': display_name,
            'url': url_final
        })

    # Контекстти түзүү
    context = {
        'menu_links': menu_links,
        'page_title': 'Dashboard',
        'is_list_view': False  # list_template'тин иштеп жатканын текшерүү үчүн
    }

    if model_name == 'dashboard':
        # Башкы бет үчүн
        return render(request, 'dashboard.html', context)

    # ------------------------------------------------------------------
    # ЭНДПОЙНТТОР ҮЧҮН ЛОГИКА (Учителя, Студенты ж.б.)
    # ------------------------------------------------------------------

    if model_name in model_map:
        ModelClass = model_map[model_name]

        # Маалыматтарды алуу (Түз DB'ден)
        try:
            object_list = ModelClass.objects.all().order_by('-id')[:10]
        except Exception:
            object_list = []  # Эгерде DB ката кетсе

        context['page_title'] = model_name.replace('_', ' ').capitalize()
        context['object_list'] = object_list
        context['model_name'] = model_name
        context['is_list_view'] = True

        # list_template.html'ди dashboard.html'дин ичине жүктөйт
        return render(request, 'list_template.html', context)

    # Эгерде модел табылбаса, башкы бетке кайтаруу
    return render(request, 'dashboard.html', context)