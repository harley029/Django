# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем переменную среды для работы Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*


# Создаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt /app/

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения
COPY . /app/

# Устанавливаем стандартный порт для работы
EXPOSE 8000

RUN python manage.py collectstatic --noinput


# Команда по умолчанию для запуска приложения
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "new_blog.wsgi:application"]
