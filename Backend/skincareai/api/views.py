# from django.shortcuts import render
# from rest_framework import generics
# from .serializers import MessageSerializer
# from .models import Message 
# from rest_framework.viewsets import ModelViewSet
# # Create your views here.

# #Here we'll create all our endpoints

# #First tutorial
# # class MessageView(generics.CreateAPIView): # CreateAPIView shows only 1 user, ListAPIView show the whole, but it's not allowed now
# #     queryset = Message.objects.all()
# #     serializer_class = MessageSerializer

# #INtegration Tutorial
# class MessageView(ModelViewSet): 
#     queryset = Message.objects.all()
#     serializer_class = MessageSerializer



from rest_framework.viewsets import ModelViewSet  #((CHATGPT CORRECTED))
from .models import Message
from .serializers import MessageSerializer

class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

