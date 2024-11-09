# skin_care_project/urls.py

from django.contrib import admin
from django.urls import path
from skin_care import views  # Make sure this import is correct

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Root URL mapped to home view
    path('api/skin-care-suggestions/', skin_care_suggestion, name='skin_care_suggestions'),  # API route

]
