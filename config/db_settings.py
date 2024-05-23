# Настройки подключения рутового пользователя PostgreSQL
ROOT_DATABASE = {
    'dbname': 'postgres',
    'user': 'postgres',  # Рутовый пользователь
    'password': 'postgres',  # Пароль рутового пользователя
    'host': 'localhost',
    'port': '5432',
}

# Настройки целевой базы данных
PRODUCT_DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'greenmap_db',
        'USER': 'greenmap_db_user',
        'PASSWORD': 'Qaz123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
