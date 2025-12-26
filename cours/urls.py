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
    if request.user.is_authenticated:
        if not request.user.is_superuser:
            return redirect('logout')
        else:
            return redirect('dashboard')
    return redirect('login')

urlpatterns = [
    # 1. ПОРТАЛ - Эң биринчи ушул ачылат
    path('', login_portal, name='portal'),

    # 2. АВТОРИЗАЦИЯ ЖАНА РОЛДУ ТЕКШЕРҮҮ (Маанилүү бөлүк)
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='portal'), name='logout'),
    path('check-role/', dashboard_redirect, name='check_role'),

    # 3. МУГАЛИМДИН ТИРКЕМЕСИ (Админдин тизмесинен жогору болушу шарт!)
    path('teacher/', include('teacher.urls')),
    path('student/', include('student.urls')),

    # 4. АДМИН ПАНЕЛ (Атын 'dashboard' деп кыскарттык, settings.py менен дал келиши үчүн)
    path('dashboard/', list_view, {'model_name': 'dashboard'}, name='dashboard'),
    path('admin-portal-check/', admin_portal_check, name='admin_portal_check'),
    path('analytics/', list_view, {'model_name': 'analytics'}, name='analytics'),

    # 5. УНИВЕРСАЛДУУ CRUD (Администратор үчүн гана)
    path('list/<str:model_name>/', list_view, name='list_view'),
    path('list/<str:model_name>/add/', add_item_view, name='add_item'),
    path('list/<str:model_name>/edit/<int:item_id>/', edit_item_view, name='edit_item'),
    path('list/<str:model_name>/delete/<int:item_id>/', delete_item_view, name='delete_item'),

    # 6. СИСТЕМАЛЫК ШИЛТЕМЕЛЕР
    path('admin/', admin.site.urls),
    path('api/', include('nur_comp.urls')),
    path('swagger/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]