"""
URL configuration for skincareai project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from api.urls import message_router  # Import the router here

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/' , include('skincareai.api.urls')),

    # Include the `api` app URLs here
    path('api/', include(message_router.urls)),  # Include router URLs here
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.contrib import admin
from django.urls import path, include

