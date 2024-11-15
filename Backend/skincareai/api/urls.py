# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import MessageView


# #First Tutorial
# # urlpatterns = [
# #     path('' , MessageView.as_view()),
# # ]

# #Integration Tutorial

# # Set up the router for the API app
# message_router = DefaultRouter()
# # message_router.register(r'messages', MessageView)
# message_router.register(r'messages', MessageView, basename='message')

# # URL patterns for the `api` app, exposing the router URLs
# urlpatterns = [
#     path('', include(message_router.urls)),  # Directly include the message_router
# ]


from django.urls import path, include
from rest_framework.routers import DefaultRouter  #((CHATGPT CORRECTED))
from .views import MessageViewSet 

message_router = DefaultRouter()
message_router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(message_router.urls)),
]
