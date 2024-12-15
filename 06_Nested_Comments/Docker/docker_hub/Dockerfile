FROM postgres:13 AS builder

RUN apt-get update && apt-get install -y python3-pip python3-venv netcat-openbsd

WORKDIR /app
COPY requirements.txt /app/requirements.txt

RUN python3 -m venv /app/venv && \
    . /app/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /app

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=8lyrMibko
ENV POSTGRES_DB=new_blog
ENV DATABASE_HOST=localhost

# Инициализация кластера и применение миграций в одном RUN:
# 1. Инициализируем БД
# 2. Запускаем PostgreSQL
# 3. Ждём готовности
# 4. Применяем миграции и создаём суперпользователя
# 5. Останавливаем PostgreSQL
ENV DJANGO_SUPERUSER_PASSWORD=admin
RUN mkdir -p /var/lib/postgresql/data && chown -R postgres:postgres /var/lib/postgresql && \
    su postgres -c "initdb -D /var/lib/postgresql/data" && \
    su postgres -c "pg_ctl start -D /var/lib/postgresql/data" && \
    bash -c "while ! nc -z localhost 5432; do sleep 1; done" && \
    # Создаём базу данных
    su postgres -c "psql --username postgres -c \"CREATE DATABASE $POSTGRES_DB OWNER $POSTGRES_USER;\"" && \
    # Активируем виртуальное окружение и применяем миграции
    . /app/venv/bin/activate && \
    python /app/manage.py migrate && \
    python /app/manage.py createsuperuser --no-input --username=admin --email=admin@example.com && \
    su postgres -c "pg_ctl stop -D /var/lib/postgresql/data"


# Финальный образ
FROM postgres:13
RUN apt-get update && apt-get install -y python3-pip
WORKDIR /app

# Копируем приложение и виртуальное окружение
COPY --from=builder /app /app
COPY --from=builder /var/lib/postgresql/data /var/lib/postgresql/data

RUN mkdir -p /app/media && chown -R postgres:postgres /app/media && chmod -R 0777 /app/media

RUN chown -R postgres:postgres /var/lib/postgresql/data && chmod -R 0700 /var/lib/postgresql/data

ENV POSTGRES_USER=${DATABASE_USER}
ENV POSTGRES_PASSWORD=${DATABASE_PASSWORD}
ENV POSTGRES_DB=${DATABASE_NAME}
ENV DJANGO_SETTINGS_MODULE=new_blog.settings

EXPOSE 8000

CMD su postgres -c "pg_ctl start -D /var/lib/postgresql/data && \
    sleep 5 && \
    . /app/venv/bin/activate && \
    python /app/manage.py runserver 0.0.0.0:8000"