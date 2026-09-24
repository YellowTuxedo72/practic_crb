FROM python:3.13-slim

# Не создаём .pyc и сразу выводим логи в консоль
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Рабочая директория контейнера
WORKDIR /app

# Копируем зависимости отдельно,
# чтобы Docker мог использовать кеш при пересборке
COPY requirements.txt .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Собираем статические файлы
RUN python manage.py collectstatic --noinput

# Запускаем Django через Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]