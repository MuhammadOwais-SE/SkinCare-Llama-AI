"""
ASGI config for mybackend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
# importing fastAPI for route
from fastapi import FastAPI
from fastapi_app import app as fastapi_app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mybackend.settings')

application = get_asgi_application()


# Mount the Django and FastAPI apps under a single ASGI server
from starlette.middleware.wsgi import WSGIMiddleware
from starlette.middleware import Middleware

# Combine both applications
from fastapi.middleware.wsgi import WSGIMiddleware

app = FastAPI()
app.mount("/django", WSGIMiddleware(django_asgi_app))
app.mount("/fastapi", fastapi_app)