from django import forms
from .models import (
    ListStudent, ListTeacher, Group, Branch, Service,
    Category, Subject, AnalyticsReport
)

class StudentForm(forms.ModelForm):
    class Meta:
        model = ListStudent
        fields = '__all__'

class TeacherForm(forms.ModelForm):
    class Meta:
        model = ListTeacher
        fields = '__all__'

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'

class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = '__all__'

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'

class AnalyticsReportForm(forms.ModelForm):
    class Meta:
        model = AnalyticsReport
        fields = '__all__'