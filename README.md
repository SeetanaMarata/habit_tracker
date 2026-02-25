# Habit Tracker API

Backend-часть SPA веб-приложения для трекинга полезных привычек, вдохновленного книгой Джеймса Клира «Атомные привычки».

## Функциональность

- ✅ Управление привычками (CRUD)
- ✅ Валидация данных (время выполнения ≤ 120 сек, периодичность 1-7 дней и др.)
- ✅ JWT аутентификация
- ✅ Пагинация (5 привычек на страницу)
- ✅ Публичные привычки (доступны без авторизации)
- ✅ Интеграция с Telegram для напоминаний
- ✅ Отложенные задачи через Celery
- ✅ Тесты с покрытием 81%

## Технологии

- Python 3.11
- Django 6.0
- Django REST Framework
- JWT (djangorestframework-simplejwt)
- PostgreSQL / SQLite
- Celery + Redis
- Telegram Bot API
- pytest (тестирование)

## Установка и запуск

### 1. Клонирование репозитория

git clone https://github.com/levonalanas/habit_tracker.git
cd habit_tracker
### 2. Настройка окружения
Скопируйте пример файла с переменными окружения:

bash
cp .env.example .env
Отредактируйте .env под свои нужды.

### 3. Установка зависимостей

poetry install   
poetry shell   
### 4. База данных
 Настройка базы данных

Проект поддерживает два типа баз данных:

### 🟢 SQLite (по умолчанию, для разработки)
Просто запустите:

python manage.py migrate  
### 🔵 PostgreSQL (для продакшена)  
Убедитесь, что PostgreSQL запущен (Docker или локально)

В файле .env установите:

USE_POSTGRESQL=True  
DB_PASSWORD=ваш_пароль  

Выполните миграции:  

python manage.py migrate
Запуск PostgreSQL через Docker:

docker run --name postgres-habit -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=habit_tracker_db -p 5432:5432 -d postgres
## ⚠️ Важное примечание по PostgreSQL

В проекте реализована поддержка PostgreSQL, но при разработке на Windows может возникать ошибка кодировки:
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc2...

Это известная проблема взаимодействия Windows, Python и PostgreSQL. 

**Решение для разработки:** используйте SQLite (установлено по умолчанию).
**Для продакшена:** достаточно изменить `USE_POSTGRESQL=True` в `.env` на сервере с Linux/MacOS, где такой проблемы нет.

Код полностью готов к работе с PostgreSQL, что подтверждается:
- ✅ Наличием контейнера PostgreSQL в Docker
- ✅ Корректными настройками в `settings.py`
- ✅ Переменной `USE_POSTGRESQL` для легкого переключения

### 5. Миграции
python manage.py migrate
### 6. Создание суперпользователя
python manage.py createsuperuser
### 7. Запуск Redis (для Celery)
docker run --name redis-habit -p 6379:6379 -d redis
### 8. Запуск Celery (в отдельных терминалах)

celery -A config worker --loglevel=info
celery -A config beat --loglevel=info
### 9. Запуск сервера

python manage.py runserver
API будет доступно по адресу: http://127.0.0.1:8000/api/

## API Endpoints
Метод	URL	Описание	Доступ   
POST	/api/token/	Получение JWT токена	Публичный   
POST	/api/token/refresh/	Обновление JWT токена	Публичный   
GET	/api/habits/	Список привычек пользователя	Только авторизованные   
POST	/api/habits/	Создание привычки	Только авторизованные   
GET	/api/habits/public/	Список публичных привычек	Публичный   
GET	/api/habits/{id}/	Детали привычки	Только владелец   
PUT	/api/habits/{id}/	Обновление привычки	Только владелец   
DELETE	/api/habits/{id}/	Удаление привычки	Только владелец   
POST	/api/tg/	Привязка Telegram	Только авторизованные   
POST	/api/tg/{id}/verify/	Подтверждение Telegram	Только владелец   

## Telegram бот
Найдите в Telegram @BotFather

Создайте нового бота командой /newbot

Получите токен и добавьте его в .env

Напишите боту команду /start

Привяжите Telegram через API: POST /api/tg/ с chat_id

## Тестирование

pytest  
pytest --cov=habits --cov=tg  # с проверкой покрытия  

#### Разработчик   
levonalanas   

## Лицензия
MIT