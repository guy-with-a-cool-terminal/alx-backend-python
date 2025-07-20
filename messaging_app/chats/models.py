import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUser(AbstractUser):
    """ extends inbuilt User model since we want to include fields such as phone number and role """
    user_id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20,null=True,blank=True)
    password = models.CharField(max_length=128)
    
    ROLE_CHOICES =[
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10,choices=ROLE_CHOICES,default='guest')
    created_at = models.DateTimeField(default=timezone.now)
    
    # we update the username field to use email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']
    
    def __str__(self):
        return f"{self.email} ({self.role})"
    
# conversations model
class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    participants = models.ManyToManyField(CustomUser,related_name='conversations')
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Conversation {self.conversation_id}"

# message model
class Message(models.Model):
    """ a message sent by a user in a convo """
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    conversation = models.ForeignKey(Conversation,on_delete=models.CASCADE,related_name='messages')
    message_body = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"From {self.sender.email} at {self.sent_at}"