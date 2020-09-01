"""
WSGI config for contacts project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
#export APPLICATION_ENV="fmicro1"
env = os.environ.get("APPLICATION_ENV", "dev")

if  env == 'local':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'contacts.settings.local')
elif env == 'qa':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'contacts.settings.qa')
elif env == 'dev':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'contacts.settings.dev')
elif env == 'staging':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'contacts.settings.staging')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'contacts.settings.production')

application = get_wsgi_application()
