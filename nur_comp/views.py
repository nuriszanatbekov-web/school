from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from django.urls import reverse

# REST Framework
from rest_framework import viewsets, filters
from rest_framework.routers import DefaultRouter, APIRootView
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend

# --- МОДЕЛДЕР, ФОРМАЛАР ЖАНА СЕРИАЛИЗЕРЛЕР ---
from .models import (
    ListStudent, ListTeacher, Group, Branch, Service,
    Category, Subject, AnalyticsReport
)
from .forms import (
    StudentForm, TeacherForm, GroupForm, BranchForm,
    ServiceForm, CategoryForm, SubjectForm, AnalyticsReportForm
)
from .serializers import (
    StudentSerializer, TeacherSerializer, GroupSerializer,
    BranchSerializer, ServiceSerializer, CategorySerializer,
    SubjectSerializer, AnalyticsReportSerializer,
    TeacherListSerializer, StudentListSerializer, GroupListSerializer,
    BranchListSerializer, ServiceListSerializer, CategoryListSerializer,
    SubjectListSerializer, AnalyticsReportListSerializer
)


# -----------------------------------------------------
# 1. ЖАРДАМЧЫ ФУНКЦИЯЛАР
# -----------------------------------------------------

def is_admin(user):
    return user.is_superuser


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


# -----------------------------------------------------
# 2. АДМИН ПАНЕЛ ҮЧҮН VIEW'ЛАР (HTML)
# -----------------------------------------------------

@login_required(login_url='/login/')
@user_passes_test(is_admin, login_url='/login/')
def list_view(request, model_name='dashboard'):
    # 1. Биринчи context өзгөрмөсүн түзүп алабыз
    context = {}

    if model_name == 'dashboard':
        # 2. Эми аны маалыматтар менен толтурабыз
        context.update({
            'teachers_count': ListTeacher.objects.count(),
            'students_count': ListStudent.objects.count(),
            'groups_count': Group.objects.count(),
            'branches_count': Branch.objects.count(),
        })
        # 3. render функциясына context'ти жиберебиз
        return render(request, 'dashboard.html', context)
    # Тизмелер үчүн
    ModelClass, _ = get_config(model_name)
    if not ModelClass:
        return redirect('dashboard')

    context = {
        'page_title': model_name.capitalize(),
        'object_list': ModelClass.objects.all().order_by('-id'),
        'model_name': model_name,
        'is_list_view': True
    }
    return render(request, 'list_template.html', context)


@login_required(login_url='/login/')
@user_passes_test(is_admin, login_url='/login/')
def add_item_view(request, model_name):
    ModelClass, FormClass = get_config(model_name)
    if not ModelClass: return redirect('dashboard')

    form = FormClass(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('list_view', model_name=model_name)

    return render(request, 'edit_template.html', {'form': form, 'model_name': model_name, 'page_title': 'Кошуу'})


@login_required(login_url='/login/')
@user_passes_test(is_admin, login_url='/login/')
def edit_item_view(request, model_name, item_id):
    ModelClass, FormClass = get_config(model_name)
    item = get_object_or_404(ModelClass, id=item_id)

    form = FormClass(request.POST or None, request.FILES or None, instance=item)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('list_view', model_name=model_name)

    return render(request, 'edit_template.html',
                  {'form': form, 'item': item, 'model_name': model_name, 'page_title': 'Түзөтүү'})


@login_required(login_url='/login/')
@user_passes_test(is_admin, login_url='/login/')
def delete_item_view(request, model_name, item_id):
    ModelClass, _ = get_config(model_name)
    if ModelClass:
        item = get_object_or_404(ModelClass, id=item_id)
        item.delete()
    return redirect('list_view', model_name=model_name)


# -----------------------------------------------------
# 3. API VIEWSET'ТЕР (DRF)
# -----------------------------------------------------

class CustomAPIRootView(APIRootView):
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CustomRouter(DefaultRouter):
    APIRootView = CustomAPIRootView


# API ViewSets (Бардыгы толук)
@extend_schema(tags=['Teachers'])
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = ListTeacher.objects.all().order_by('fio')
    serializer_class = TeacherSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['tag', 'branch']
    search_fields = ['fio']

    def get_serializer_class(self): return TeacherListSerializer if self.action == 'list' else TeacherSerializer


@extend_schema(tags=['Students'])
class StudentViewSet(viewsets.ModelViewSet):
    queryset = ListStudent.objects.all().order_by('full_name')
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['full_name']

    def get_serializer_class(self): return StudentListSerializer if self.action == 'list' else StudentSerializer


@extend_schema(tags=['Groups'])
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer

    def get_serializer_class(self): return GroupListSerializer if self.action == 'list' else GroupSerializer


@extend_schema(tags=['Branches'])
class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all().order_by('name')
    serializer_class = BranchSerializer

    def get_serializer_class(self): return BranchListSerializer if self.action == 'list' else BranchSerializer


@extend_schema(tags=['Categories'])
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer

    def get_serializer_class(self): return CategoryListSerializer if self.action == 'list' else CategorySerializer


@extend_schema(tags=['Subjects'])
class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all().order_by('name')
    serializer_class = SubjectSerializer

    def get_serializer_class(self): return SubjectListSerializer if self.action == 'list' else SubjectSerializer


@extend_schema(tags=['Services'])
class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all().order_by('name')
    serializer_class = ServiceSerializer

    def get_serializer_class(self): return ServiceListSerializer if self.action == 'list' else ServiceSerializer


@extend_schema(tags=['Analytics'])
class AnalyticsReportViewSet(viewsets.ModelViewSet):
    queryset = AnalyticsReport.objects.all().order_by('-created_at')
    serializer_class = AnalyticsReportSerializer

    def get_serializer_class(
            self): return AnalyticsReportListSerializer if self.action == 'list' else AnalyticsReportSerializer