import os
from .settings import *

# PostgreSQL somente para testes (banco isolado)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('TEST_DB_NAME', 'agenda_test'),
        'USER': os.environ.get('TEST_DB_USER', os.environ.get('DB_USER', 'postgres')),
        'PASSWORD': os.environ.get('TEST_DB_PASSWORD', os.environ.get('DB_PASSWORD', 'postgres')),
        'HOST': os.environ.get('TEST_DB_HOST', os.environ.get('DB_HOST', 'localhost')),
        'PORT': os.environ.get('TEST_DB_PORT', os.environ.get('DB_PORT', '5432')),
    }
}
