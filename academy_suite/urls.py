from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # API Routes (Version 1)
    path('api/v1/users/', include('apps.users.api.urls')),
    path('api/v1/learning/', include('apps.learning.api.urls')),
    path('api/v1/enrollment/', include('apps.enrollment.api.urls')),
    path('api/v1/interactions/', include('apps.interactions.api.urls')),
    path('api/v1/reports/', include('apps.reports.api.urls')),

    # Frontend Routes
    path('users/', include('apps.users.urls')),
    path('learning/', include('apps.learning.urls')),
    path('interactions/', include('apps.interactions.urls')),
    path('enrollment/', include('apps.enrollment.urls')),
    path('contracts/', include('apps.contracts.urls')), # New line added here
    
    # Core app will handle main routes like login, dashboard etc.
    path('', include('apps.core.urls')),

]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)