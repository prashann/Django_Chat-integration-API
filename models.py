from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class chat_rooms(models.Model):
    chat_room_id = models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length = 100)
    created_at = models.DateTimeField(auto_now=True)

class messages(models.Model):
    message_id = models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID')
    chat_room = models.ForeignKey(chat_rooms, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now=True)