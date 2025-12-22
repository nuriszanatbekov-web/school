from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from nur_comp.views import list_view, add_item_view, edit_item_view, delete_item_view
from teacher.views import login_portal, dashboard_redirect

urlpatterns = [
    # 1. ПОРТАЛ - Колдонуучу эң биринчи көрө турган бет
    path('', login_portal, name='portal'),

    # 2. АВТОРИЗАЦИЯ
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='portal'), name='logout'),

    # 3. РОЛДУ ТЕКШЕРҮҮ (Логинден кийин ушул жерге келет)
    path('check-role/', dashboard_redirect, name='check_role'),

    # 4. АДМИН ПАНЕЛ (Сиздин жекече панелиңиз)
    path('dashboard/', list_view, {'model_name': 'dashboard'}, name='dashboard'),

    # 5. CRUD (Маалыматтарды башкаруу)
    path('list/<str:model_name>/', list_view, name='list_view'),
    path('list/<str:model_name>/add/', add_item_view, name='add_item'),
    path('list/<str:model_name>/edit/<int:item_id>/', edit_item_view, name='edit_item'),
    path('list/<str:model_name>/delete/<int:item_id>/', delete_item_view, name='delete_item'),

    # 6. МУГАЛИМДИН ТИРКЕМЕСИ
    path('teacher/', include('teacher.urls')),

    # 6.1 ОКУУЧУНУН ТИРКЕМЕСИ (УШУЛ ЖЕРДИ КОШУҢУЗ)
    path('student/', include('student.urls')),

    # 7. Django'нун стандарттык админкасы
    path('django-admin/', admin.site.urls),

    # 8. API ЖАНА ДОКУМЕНТАЦИЯ
    path('api/', include('nur_comp.urls')),
    path('swagger/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]