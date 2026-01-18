# resume_it/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('resume.urls')),
]

# Для production статика и медиа обслуживаются WhiteNoise и веб-сервером
# Но для режима DEBUG оставляем возможность локальной разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)