# courses/urls.py

from rest_framework.routers import DefaultRouter
from .views import (
    TeacherViewSet, StudentViewSet, GroupViewSet, BranchViewSet,
    CategoryViewSet, SubjectViewSet, ServiceViewSet, AnalyticsReportViewSet
)

router = DefaultRouter()

# --- Сиздин талап кылган 7+ эндпойнттор ---

router.register(r'teachers', TeacherViewSet)         # 1. Мугалимдер
router.register(r'students', StudentViewSet)         # 2. Окуучулар
router.register(r'groups', GroupViewSet)             # 3. Группалар (Класстар)
router.register(r'branches', BranchViewSet)         # 4. Филиалдар
router.register(r'services', ServiceViewSet)         # 5. Кызматтар
router.register(r'categories', CategoryViewSet)     # 6. Категориялар
router.register(r'subjects', SubjectViewSet)         # 7. Предметтер
router.register(r'analytics', AnalyticsReportViewSet)# 8. Аналитикалык Отчеттор

# -----------------------------------------

urlpatterns = router.urls