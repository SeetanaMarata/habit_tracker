import os

from celery import Celery

# Устанавливаем переменную окружения для настроек Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

# Загружаем конфигурацию из настроек Django, используя пространство имен 'CELERY'
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматически находим задачи в приложениях
app.autodiscover_tasks()
