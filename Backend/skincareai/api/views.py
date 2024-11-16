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



# from rest_framework.viewsets import ModelViewSet  #((CHATGPT CORRECTED))
# from .models import Message
# from .serializers import MessageSerializer

# class MessageViewSet(ModelViewSet):
#     queryset = Message.objects.all()
#     serializer_class = MessageSerializer


# api/views.py

from rest_framework.viewsets import ModelViewSet
from .models import Message
from .serializers import MessageSerializer
from .service import fetch_gemini_data

from api.service import test_import
print(test_import())


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        prompt_text = request.data.get('message_text')
        image = request.FILES.get('image', None)  # Handling image as optional
        is_ai_response = False  # Assuming this is always False when creating from user input

        # Fetch AI response from Gemini API
        ai_response = fetch_gemini_data(prompt_text)
        if ai_response is None:
            return Response({'error': 'AI response not available'}, status=status.HTTP_400_BAD_REQUEST)

        user_message = Message.objects.create(
            message_text=prompt_text,
            is_ai_response=False,
            image=image
        )

        ai_message = Message.objects.create(
            message_text=ai_response,
            is_ai_response=True
        )

        serializer = self.get_serializer([user_message, ai_message], many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
