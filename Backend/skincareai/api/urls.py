from django.urls import path
from . import views

urlpatterns = [
    path('api/messages/', views.create_message, name='create_message'),
]
