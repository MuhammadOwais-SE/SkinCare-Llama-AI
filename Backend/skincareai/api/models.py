from django.db import models
import uuid

# User model with AutoField as primary key instead of UUIDField
class User(models.Model):
    user_id = models.AutoField(primary_key=True)  # Change to AutoField for sequential IDs
    username = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username or str(self.user_id)

# Conversation model with AutoField as primary key
class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conversations")
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Conversation {self.conversation_id} with User {self.user.user_id}"



# Message model with AutoField as primary key
class Message(models.Model):
    message_id = models.AutoField(primary_key=True)  # Change to AutoField for sequential IDs
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages", null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages", null=True)
    message_text = models.TextField()
    is_ai_response = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="messages/", blank=True, null=True)

    def __str__(self):
        sender = "AI" if self.is_ai_response else "User"
        return f"{sender} message in Conversation {self.conversation.conversation_id}"
