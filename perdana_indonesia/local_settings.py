import os

import dotenv
from django.conf import settings

dotenv_file = os.path.join(settings.BASE_DIR, "../.env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

DEBUG = True
USE_TZ = False
LANGUAGE_CODE = 'id'
CORS_ORIGIN_ALLOW_ALL = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'perdana_indonesia_db'),
        'USER': os.environ.get("DB_USER", 'root'),
        'PASSWORD': os.environ.get("DB_PASSWORD", 'masuk123'),
        'HOST': os.environ.get("DB_HOST", 'localhost'),
        'PORT': os.environ.get("DB_PORT", '3306'),
        'TEST': {
            'NAME': os.environ.get('TEST_DB_NAME', 'perdana_indonesia_test_db'),
        },
    }
}

# Use this if deploy on heroku
# import dj_database_url
# DATABASES['default'] = dj_database_url.config(conn_max_age=600)
