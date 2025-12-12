from rest_framework import serializers
from .models import (
    ListStudent, ListTeacher, Group, Branch, Service,
    Category, Subject, AnalyticsReport
)

# ===================================================
# LIST SERIALIZERS (Кыска версиялар)
# ===================================================

class BranchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id', 'name', 'address', 'phone']


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class SubjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'category']


class TeacherListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListTeacher
        fields = ['id', 'fio', 'phone_number', 'tag']


class GroupListSerializer(serializers.ModelSerializer):
    subject = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'subject', 'is_active']


class StudentListSerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(read_only=True)
    branch = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ListStudent
        fields = ['id', 'full_name', 'group', 'branch']


class ServiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'price', 'description']


class AnalyticsReportListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyticsReport
        fields = ['id', 'title', 'created_at', 'data']


# ===================================================
# DETAIL SERIALIZERS (Толук версиялар)
# ===================================================

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListTeacher
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListStudent
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class AnalyticsReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyticsReport
        fields = '__all__'
