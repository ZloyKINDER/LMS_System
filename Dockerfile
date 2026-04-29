FROM python:3.13-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    nginx \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN pip install poetry

# Копирование файлов с зависимостями
COPY pyproject.toml poetry.lock /app/

# Настройка Poetry - НЕ создавать виртуальное окружение
RUN poetry config virtualenvs.create false

# Установка зависимостей (включая Celery)
RUN poetry install --no-interaction --no-ansi --no-root

# Добавляем PATH для бинарников Poetry
ENV PATH="/root/.local/bin:${PATH}"

# Копирование остального проекта
COPY . .

# Копирование конфигурации Nginx
COPY nginx.conf /etc/nginx/sites-available/default

# Копирование конфигурации Supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Создание директорий для статики и медиа
RUN mkdir -p /app/static /app/media /app/logs

# Сбор статики
RUN python manage.py collectstatic --noinput

# Настройка переменных окружения
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=config.settings

# Открываем порты
EXPOSE 80

# Запуск Supervisor (который запустит Gunicorn, Nginx, Celery)
CMD ["supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]