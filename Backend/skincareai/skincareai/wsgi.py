"""
<<<<<<<< HEAD:Backend/skin_care_project/skin_care_project/wsgi.py
WSGI config for skin_care_project project.
========
WSGI config for skincareai project.
>>>>>>>> 475dfdc22fca0bd96a514992bfe73800f011ee35:Backend/skincareai/skincareai/wsgi.py

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

<<<<<<<< HEAD:Backend/skin_care_project/skin_care_project/wsgi.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skin_care_project.settings')
========
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skincareai.settings')
>>>>>>>> 475dfdc22fca0bd96a514992bfe73800f011ee35:Backend/skincareai/skincareai/wsgi.py

application = get_wsgi_application()
