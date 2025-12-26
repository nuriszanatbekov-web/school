from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from rest_framework import viewsets, filters # 'filters

# REST Framework
from rest_framework import viewsets, filters as drf_filters
from rest_framework.routers import DefaultRouter, APIRootView
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend

# --- МОДЕЛДЕР ЖАНА ФОРМАЛАР ---
from .models import (
    ListStudent, ListTeacher, Group, Branch, Service,
    Category, Subject, AnalyticsReport
)
from .forms import (
    StudentForm, TeacherForm, GroupForm, BranchForm,
    ServiceForm, CategoryForm, SubjectForm, AnalyticsReportForm
)
from .serializers import *

# -----------------------------------------------------
# 1. ЖАРДАМЧЫ ФУНКЦИЯЛАР
# -----------------------------------------------------

def is_admin(user):
    return user.is_authenticated and user.is_superuser

def get_config(model_name):
    """ Ар бир модель үчүн конфигурацияны тактоо """
    configs = {
        'teachers': (ListTeacher, TeacherForm, 'fio'),
        'students': (ListStudent, StudentForm, 'full_name'),
        'groups': (Group, GroupForm, 'name'),
        'branches': (Branch, BranchForm, 'name'),
        'services': (Service, ServiceForm, 'name'),
        'categories': (Category, CategoryForm, 'name'),
        'subjects': (Subject, SubjectForm, 'name'),
        'analytics': (AnalyticsReport, AnalyticsReportForm, 'title'),
    }
    return configs.get(model_name, (None, None, None))

# -----------------------------------------------------
# 2. АДМИН ПАНЕЛ (HTML VIEWS)
# -----------------------------------------------------

@login_required(login_url='/login/')
@user_passes_test(is_admin, login_url='/login/')
def list_view(request, model_name='dashboard'):
    context = {'model_name': model_name}

    # Дашборд статистикасы
    if model_name == 'dashboard':
        context.update({
            'teachers_count': ListTeacher.objects.count(),
            'students_count': ListStudent.objects.count(),
            'groups_count': Group.objects.count(),
            'branches_count': Branch.objects.count(),
            'page_title': 'Башкаруу борбору',
        })
        return render(request, 'dashboard.html', context)

    ModelClass, _, search_field = get_config(model_name)
    if not ModelClass:
        messages.error(request, "Бул бөлүм табылган жок.")
        return redirect('dashboard')

    object_list = ModelClass.objects.all().order_by('-id')

    # Издөө логикасы (Универсалдуу)
    query = request.GET.get('search')
    if query and search_field:
        filter_kwargs = {f"{search_field}__icontains": query}
        object_list = object_list.filter(**filter_kwargs)

    # Verbose name аркылуу титулду кыргызча чыгаруу
    verbose_name = ModelClass._meta.verbose_name_plural or model_name.capitalize()

    context.update({
        'page_title': verbose_name,
        'object_list': object_list,
        'search_query': query,
    })
    return render(request, 'list_template.html', context)

@login_required(login_url='/login/')
@user_passes_test(is_admin, login_url='/login/')
def add_item_view(request, model_name):
    ModelClass, FormClass, _ = get_config(model_name)
    if not ModelClass: return redirect('dashboard')

    if request.method == 'POST':
        form = FormClass(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f"Жаңы маалымат ийгиликтүү кошулду.")
            return redirect('list_view', model_name=model_name)
    else:
        form = FormClass()

    return render(request, 'edit_template.html', {
        'form': form,
        'model_name': model_name,
        'page_title': 'Жаңы кошуу'
    })

@login_required(login_url='/login/')
@user_passes_test(is_admin, login_url='/login/')
def edit_item_view(request, model_name, item_id):
    ModelClass, FormClass, _ = get_config(model_name)
    item = get_object_or_404(ModelClass, id=item_id)

    if request.method == 'POST':
        form = FormClass(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Өзгөртүүлөр ийгиликтүү сакталды.")
            return redirect('list_view', model_name=model_name)
    else:
        form = FormClass(instance=item)

    return render(request, 'edit_template.html', {
        'form': form,
        'item': item,
        'model_name': model_name,
        'page_title': 'Маалыматты түзөтүү'
    })

@login_required(login_url='/login/')
@user_passes_test(is_admin, login_url='/login/')
def delete_item_view(request, model_name, item_id):
    ModelClass, _, _ = get_config(model_name)
    if ModelClass:
        item = get_object_or_404(ModelClass, id=item_id)
        item.delete()
        messages.warning(request, "Маалымат системадан өчүрүлдү.")
    return redirect('list_view', model_name=model_name)

# -----------------------------------------------------
# 3. API VIEWSET'ТЕР (DRF БӨЛҮГҮ)
# -----------------------------------------------------

class CustomAPIRootView(APIRootView):
    """ API баштапкы бетин кооздоо """
    pass

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