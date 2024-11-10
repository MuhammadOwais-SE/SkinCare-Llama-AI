"""
WSGI config for skincareai project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Set the default settings module for the 'skincareai' project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skincareai.settings')

application = get_wsgi_application()
