from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('message_id', 'message_text', 'is_ai_response', 'created_at')  # 'conversation', 'user',
        