from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    list_view, add_item_view, edit_item_view, delete_item_view,
    CustomRouter, CustomAPIRootView,
    TeacherViewSet, StudentViewSet, GroupViewSet,
    BranchViewSet, CategoryViewSet, SubjectViewSet,
    ServiceViewSet, AnalyticsReportViewSet
)

# 1. API үчүн Роутерди түзүү
router = CustomRouter()
router.register('teachers', TeacherViewSet, basename='teacher')
router.register('students', StudentViewSet, basename='student')
router.register('groups', GroupViewSet, basename='group')
router.register('branches', BranchViewSet, basename='branch')
router.register('categories', CategoryViewSet, basename='category')
router.register('subjects', SubjectViewSet, basename='subject')
router.register('services', ServiceViewSet, basename='service')
router.register('analytics', AnalyticsReportViewSet, basename='analytics')

# 2. Негизги багыттар (URL Patterns)
urlpatterns = [
    # --- НЕГИЗГИ ПАНЕЛЬ ЖАНА ТИЗМЕЛЕР ---
    path('dashboard/', list_view, name='dashboard'),
    path('list/<str:model_name>/', list_view, name='list_view'),

    # --- КУРАЛДАР (Кошуу, Түзөтүү, Өчүрүү) ---
    path('add/<str:model_name>/', add_item_view, name='add_item'),
    path('edit/<str:model_name>/<int:item_id>/', edit_item_view, name='edit_item'),
    path('delete/<str:model_name>/<int:item_id>/', delete_item_view, name='delete_item'),

    # --- АВТОРИЗАЦИЯ (Логин / Чыгуу) ---
    # Бул жер маанилүү! Logout иштеши үчүн керек:
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # --- API БӨЛҮГҮ ---
    path('api-root/', router.get_api_root_view(CustomAPIRootView), name='api-root'),
]

# API роутердин URL даректерин кошуу
urlpatterns += router.urls