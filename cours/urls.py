from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),

    # API Жолу: http://127.0.0.1:8000/api/
    path('api/', include('nur_comp.urls')),

    # SWAGGER UI: http://127.0.0.1:8000/swagger/
    path('swagger/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]