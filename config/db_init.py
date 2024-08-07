import sys
import os

# Добавление пути проекта в PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django
from django.core.management import call_command
from django.contrib.auth import get_user_model
import psycopg2
from psycopg2 import sql
from config import db_settings

ROOT_DATABASE = db_settings.ROOT_DATABASE
DATABASES = db_settings.PRODUCT_DATABASES

# Настройки суперпользователя
SUPERUSER_DETAILS = {
    'email': 'admin@example.com',
    'password': 'Qaz123',
}


def create_database_and_user():
    conn = psycopg2.connect(
        dbname=ROOT_DATABASE['dbname'],
        user=ROOT_DATABASE['user'],
        password=ROOT_DATABASE['password'],
        host=ROOT_DATABASE['host'],
        port=ROOT_DATABASE['port']
    )
    conn.autocommit = True
    cursor = conn.cursor()

    # Проверка существования базы данных
    cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DATABASES['default']['NAME']}'")
    exists = cursor.fetchone()
    if not exists:
        # Создание пользователя базы данных
        try:
            cursor.execute(
                sql.SQL("CREATE USER {} WITH PASSWORD %s").format(
                    sql.Identifier(DATABASES['default']['USER'])
                ),
                [DATABASES['default']['PASSWORD']]
            )
            print(f"Пользователь {DATABASES['default']['USER']} успешно создан")
        except psycopg2.errors.DuplicateObject:
            print(f"Пользователь {DATABASES['default']['USER']} уже существует")

        # Создание базы данных
        cursor.execute(
            sql.SQL("CREATE DATABASE {} OWNER {}").format(
                sql.Identifier(DATABASES['default']['NAME']),
                sql.Identifier(DATABASES['default']['USER'])
            )
        )
        print(f"База данных {DATABASES['default']['NAME']} успешно создана")
    else:
        print(f"База данных {DATABASES['default']['NAME']} уже существует")

    cursor.close()
    conn.close()


def apply_migrations():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MapGreen.settings')
    django.setup()
    call_command('makemigrations')
    call_command('migrate')


def create_superuser():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MapGreen.settings')
    django.setup()

    User = get_user_model()

    if not User.objects.filter(email=SUPERUSER_DETAILS['email']).exists():
        User.objects.create_superuser(
            email=SUPERUSER_DETAILS['email'],
            password=SUPERUSER_DETAILS['password']
        )
        print(f"Суперпользователь {SUPERUSER_DETAILS['email']} успешно создан")
    else:
        print(f"Суперпользователь {SUPERUSER_DETAILS['email']} уже существует")


if __name__ == '__main__':
    print("1. Запуск скрипта инициализации базы данных...")
    try:
        create_database_and_user()
    except Exception as e:
        print(f"Произошла ошибка при создании базы данных: {e}")
    print("2. Применение миграций...")
    try:
        apply_migrations()
        print("Миграции успешно применены")
    except Exception as e:
        print(f"Произошла ошибка при применении миграций: {e}")
    print("3. Создание суперпользователя...")
    try:
        create_superuser()
    except Exception as e:
        print(f"Произошла ошибка при создании суперпользователя: {e}")
