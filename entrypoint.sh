#!/bin/sh

# Применяем миграции базы данных
python manage.py migrate --noinput

# Собираем статические файлы (для админки)
python manage.py collectstatic --noinput

# Запускаем сервер Gunicorn (он лучше чем runserver для продакшена)
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000