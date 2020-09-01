#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
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

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
