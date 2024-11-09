from django.urls import path
from . import views
from django.conf import settings


urlpatterns = [
    path('suggestions/', views.skin_care_suggestion, name='skin_care_suggestion'),
]
