from django.db import models

# Create your models here.
class UserData(models.Model):
    prompt_history = models.JSONField()  # Store the prompt history for multi-conversion
    prompt_text = models.TextField()  # Stores the text prompt from the user
    image = models.ImageField(upload_to='user_images/', null=True, blank=True)  # Optional image upload
