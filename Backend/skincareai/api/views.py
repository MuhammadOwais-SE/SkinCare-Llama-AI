from django.shortcuts import render
from rest_framework import generics
from .serializers import MessageSerializer
from .models import Message 
# Create your views here.

#Here we'll create all our endpoints

class MessageView(generics.CreateAPIView): # CreateAPIView shows only 1 user, ListAPIView show the whole, but it's not allowed now
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

