from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# Views'тарды импорттоо
from nur_comp.views import list_view, add_item_view, edit_item_view, delete_item_view
from teacher.views import login_portal, dashboard_redirect

# ПОРТАЛДАГЫ АДМИН БАСКЫЧЫ ҮЧҮН ТЕКШЕРҮҮ ФУНКЦИЯСЫ
def admin_portal_check(request):
    """
    Эгер колдонуучу мугалим катары кирип турган болсо, аны чыгарып (logout),
    админ катары кирүү үчүн логин барагына жиберет.
    """
    if request.user.is_authenticated:
        if not request.user.is_superuser:
            # Мугалимди чыгарып салуу
            return redirect('logout')
        else:
            # Эгер ал мурун эле админ болсо, түз дашбордго
            return redirect('dashboard')
    return redirect('login')

urlpatterns = [
    # 1. ПОРТАЛ - Биринчи ушул ачылат
    path('', login_portal, name='portal'),

    # 2. АДМИНДИ ТЕКШЕРҮҮ (Порталдагы баскыч үчүн)
    path('admin-portal-check/', admin_portal_check, name='admin_portal_check'),

    # 3. АВТОРИЗАЦИЯ
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    # Logout болгондо кайра порталга же логинге багыттоо
    path('logout/', auth_views.LogoutView.as_view(next_page='portal'), name='logout'),

    # 4. РОЛДУ ТЕКШЕРҮҮ
    path('check-role/', dashboard_redirect, name='check_role'),

    # 5. АДМИН ПАНЕЛ ЖАНА АНАЛИТИКА
    path('dashboard/', list_view, {'model_name': 'dashboard'}, name='admin_dashboard'),
    path('analytics/', list_view, {'model_name': 'analytics'}, name='analytics'),

    # 6. CRUD (Маалыматтарды башкаруу)
    path('list/<str:model_name>/', list_view, name='list_view'),
    path('list/<str:model_name>/add/', add_item_view, name='add_item'),
    path('list/<str:model_name>/edit/<int:item_id>/', edit_item_view, name='edit_item'),
    path('list/<str:model_name>/delete/<int:item_id>/', delete_item_view, name='delete_item'),

    # 7. ТИРКЕМЕЛЕР
    path('teacher/', include('teacher.urls')),
    path('student/', include('student.urls')),

    # 8. СИСТЕМА
    path('admin/', admin.site.urls),
    path('api/', include('nur_comp.urls')),
    path('swagger/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]