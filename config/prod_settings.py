import os

import dj_database_url
import dotenv

from .settings import *

dotenv_file = os.path.join(BASE_DIR, ".env.prod")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

DATABASE_URL_SCHEMA = os.environ.get('DATABASE_URL', 'postgres://perdana@localhost:5432/perdana_db')
DATABASES['default'] = dj_database_url.parse(url=DATABASE_URL_SCHEMA, conn_max_age=600)