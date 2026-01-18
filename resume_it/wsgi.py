"""
WSGI config for resume_it project.

Production configuration with WhiteNoise for static and media files.
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_it.settings')

# Получаем стандартное WSGI приложение Django
django_app = get_wsgi_application()

# Оборачиваем в WhiteNoise для обслуживания статических файлов
application = WhiteNoise(django_app, root='/app/staticfiles')

# Добавляем медиа файлы из /data/media
application.add_files('/data/media', prefix='media')