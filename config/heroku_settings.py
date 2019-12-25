import os

import dj_database_url
import dotenv

from .settings import BASE_DIR

dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

CORS_ORIGIN_ALLOW_ALL = True

DATABASES = {}
DATABASES['default'] = dj_database_url.config(conn_max_age=600)
