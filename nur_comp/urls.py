# nur_comp/urls.py
from django.urls import path
from .views import (
    CustomRouter, CustomAPIRootView,
    TeacherViewSet, StudentViewSet, GroupViewSet,
    BranchViewSet, CategoryViewSet, SubjectViewSet,
    ServiceViewSet, AnalyticsReportViewSet
)

router = CustomRouter()
router.register('teachers', TeacherViewSet, basename='teacher')
router.register('students', StudentViewSet, basename='student')
router.register('groups', GroupViewSet, basename='group')
router.register('branches', BranchViewSet, basename='branch')
router.register('categories', CategoryViewSet, basename='category')
router.register('subjects', SubjectViewSet, basename='subject')
router.register('services', ServiceViewSet, basename='service')
router.register('analytics', AnalyticsReportViewSet, basename='analytics')

urlpatterns = [
    # Роутердин өзүнүн root view-су
    path('api-root/', router.get_api_root_view(CustomAPIRootView), name='api-root'),
]

# Сөзсүз түрдө += колдонуңуз, include('') эмес!
urlpatterns += router.urls