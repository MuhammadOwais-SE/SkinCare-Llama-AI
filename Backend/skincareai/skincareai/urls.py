"""
<<<<<<< HEAD
<<<<<<<< HEAD:Backend/skincareai/skincareai/urls.py
URL configuration for skincareai project.
========
URL configuration for skin_care_project project.
>>>>>>>> 00fc017151e8ce18683c755d3c90c0878fe2b2fa:Backend/skin_care_project/skin_care_project/urls.py
=======
<<<<<<<< HEAD:Backend/skin_care_project/skin_care_project/urls.py
URL configuration for skin_care_project project.
========
URL configuration for skincareai project.
>>>>>>>> 475dfdc22fca0bd96a514992bfe73800f011ee35:Backend/skincareai/skincareai/urls.py
>>>>>>> 99a64882e2d5eb7954e61187c31ef2053741c836

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# skin_care_project/urls.py
from django.contrib import admin
<<<<<<< HEAD
<<<<<<<< HEAD:Backend/skincareai/skincareai/urls.py
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , include('api.urls')),
========
=======
<<<<<<<< HEAD:Backend/skin_care_project/skin_care_project/urls.py
>>>>>>> 99a64882e2d5eb7954e61187c31ef2053741c836
from django.urls import path
from skin_care import views  # Add this import for views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # This should map the root URL to the home view
<<<<<<< HEAD
>>>>>>>> 00fc017151e8ce18683c755d3c90c0878fe2b2fa:Backend/skin_care_project/skin_care_project/urls.py
=======
========
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , include('api.urls')),
>>>>>>>> 475dfdc22fca0bd96a514992bfe73800f011ee35:Backend/skincareai/skincareai/urls.py
>>>>>>> 99a64882e2d5eb7954e61187c31ef2053741c836
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
