from django.db import models
import uuid

# Create your models here.

# class User(models.Model):
#     user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     username = models.CharField(max_length=255, blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.username or str(self.user_id)


# class Conversation(models.Model):
#     conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conversations")
#     started_at = models.DateTimeField(auto_now_add=True)
#     ended_at = models.DateTimeField(blank=True, null=True)

#     def __str__(self):
#         return f"Conversation {self.conversation_id} with User {self.user.user_id}"


# class Message(models.Model):
#     message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     # conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
#     # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
#     message_text = models.TextField()
#     is_ai_response = models.BooleanField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         # sender = "AI" if self.is_ai_response else "User"
#         # return f"{sender} message in Conversation {self.conversation.conversation_id}"
#         if (self.is_ai_response == True):
#             return f"AI : {self.message_text}"
#         else: 
#             return f"User : {self.message_text}"


class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message_text = models.TextField()
    is_ai_response = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)  # Optional image field

    def __str__(self):
        if self.is_ai_response:
            return f"AI: {self.message_text}"
        return f"User: {self.message_text}"
