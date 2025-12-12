from rest_framework import viewsets
from rest_framework.routers import DefaultRouter, APIRootView
from drf_spectacular.utils import extend_schema

from .models import (
    ListStudent, ListTeacher, Group, Branch, Service,
    Category, Subject, AnalyticsReport
)

from .serializers import (
    # ===================================================
    # 1. ТОЛУК СЕРИАЛИЗЕРЛЕР (8)
    # ===================================================
    StudentSerializer, TeacherSerializer, GroupSerializer,
    BranchSerializer, ServiceSerializer, CategorySerializer,
    SubjectSerializer, AnalyticsReportSerializer,

    # ===================================================
    # 2. ТИЗМЕ СЕРИАЛИЗЕРЛЕР (8) - СИЗ УНУТКАН БЛОК
    # ===================================================
    TeacherListSerializer, StudentListSerializer, GroupListSerializer,
    BranchListSerializer, ServiceListSerializer, CategoryListSerializer,
    SubjectListSerializer, AnalyticsReportListSerializer
)


# -----------------------------------------------------
# 1. CUSTOM ROUTER (IP/URL маселесин чечет)
# -----------------------------------------------------

class CustomAPIRootView(APIRootView):
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CustomRouter(DefaultRouter):
    APIRootView = CustomAPIRootView


# -----------------------------------------------------
# 2. VIEWSET'ТЕР (SERIALIZER ТАНДОО ЛОГИКАСЫ)
# -----------------------------------------------------

@extend_schema(tags=['Teachers'])
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = ListTeacher.objects.all()
    # Демейки Serializer
    serializer_class = TeacherSerializer

    def get_serializer_class(self):
        # GET /api/teachers/ үчүн (4 гана талаа)
        if self.action == 'list':
            return TeacherListSerializer
        # Башка action'дар (retrieve, create, update ж.б.) үчүн (Бардык талаалар)
        return TeacherSerializer


@extend_schema(tags=['Students'])
class StudentViewSet(viewsets.ModelViewSet):
    queryset = ListStudent.objects.all()
    serializer_class = StudentSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return StudentListSerializer
        return StudentSerializer


@extend_schema(tags=['Groups'])
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return GroupListSerializer
        return GroupSerializer


@extend_schema(tags=['Branches'])
class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return BranchListSerializer
        return BranchSerializer


@extend_schema(tags=['Categories'])
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return CategoryListSerializer
        return CategorySerializer


@extend_schema(tags=['Subjects'])
class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return SubjectListSerializer
        return SubjectSerializer


@extend_schema(tags=['Services'])
class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return ServiceListSerializer
        return ServiceSerializer


@extend_schema(tags=['Analytics'])
class AnalyticsReportViewSet(viewsets.ModelViewSet):
    queryset = AnalyticsReport.objects.all().order_by('-created_at')
    serializer_class = AnalyticsReportSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return AnalyticsReportListSerializer
        return AnalyticsReportSerializer