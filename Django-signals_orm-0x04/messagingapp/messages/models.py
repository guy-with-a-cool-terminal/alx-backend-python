from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    objects = UnreadMessagesManager()
    sender = models.ForeignKey(User,related_name='sent_messages',on_delete=models.CASCADE)
    receiver = models.ForeignKey(User,related_name='received_messages',on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    parent_message = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    read = models.BooleanField(default=False)


class Notification(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.ForeignKey(Message,on_delete=Models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class MessageHistory(models.Model):
    message = models.ForeignKey(Message,on_delete=models.CASCADE)
    old_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        return self.filter(receiver=user, read=False)
