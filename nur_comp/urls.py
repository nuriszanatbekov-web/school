from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

# 1. Роутерди түзүү
router = views.CustomRouter()
router.register('teachers', views.TeacherViewSet, basename='teacher')
router.register('students', views.StudentViewSet, basename='student')
router.register('groups', views.GroupViewSet, basename='group')
router.register('branches', views.BranchViewSet, basename='branch')
router.register('categories', views.CategoryViewSet, basename='category')
router.register('subjects', views.SubjectViewSet, basename='subject')
router.register('services', views.ServiceViewSet, basename='service')
router.register('analytics', views.AnalyticsReportViewSet, basename='analytics')

urlpatterns = [
    # API эндпоинттарды башкы жолго коюу (include ичинде бош калтырабыз)
    path('', include(router.urls)),  # Эми /api/ жазганда түз ушул жерге келет

    # API Root кооз көрүнүшү үчүн
    path('root/', router.get_api_root_view(views.CustomAPIRootView), name='api-root'),

    # --- КАЛГАН ПАТТЕРНДЕР ---
    path('dashboard/', views.list_view, {'model_name': 'dashboard'}, name='dashboard'),
    path('list/<str:model_name>/', views.list_view, name='list_view'),
    path('add/<str:model_name>/', views.add_item_view, name='add_item_view'),
    path('edit/<str:model_name>/<int:item_id>/', views.edit_item_view, name='edit_item_view'),
    path('delete/<str:model_name>/<int:item_id>/', views.delete_item_view, name='delete_item_view'),
]