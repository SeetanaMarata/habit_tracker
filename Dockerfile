# Dockerfile
FROM python:3.11-slim

# Устанавливаем зависимости для PostgreSQL и системы
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install poetry

# Создаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock* /app/

# Настраиваем Poetry: не создавать виртуальное окружение (используем системный Python)
RUN poetry config virtualenvs.create false

# Устанавливаем зависимости
RUN poetry install --no-interaction --no-ansi

# Копируем код проекта
COPY . /app/

# Делаем скрипт entrypoint исполняемым
RUN chmod +x entrypoint.sh

# Команда по умолчанию
CMD ["./entrypoint.sh"]