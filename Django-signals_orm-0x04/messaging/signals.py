from django.db.models.signals import post_save,pre_save,post_delete
from django.dispatch import receiver
from .models import Message,Notification

@receiver(post_save,sender=Message)
def create_notification(sender,instance,created,**kwargs):
    if created:
        Notification.objects.create(user=instance.receiver,message=instance)

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:  # Check if the message already exists
        old_message = Message.objects.filter(pk=instance.pk).first()  # Use filter to get the existing message
        if old_message and old_message.content != instance.content:  # Check if the content has changed
            MessageHistory.objects.create(message=old_message, old_content=old_message.content)
            instance.edited = True  # Mark the message as edited
            instance.edited_at = timezone.now()  # Set the edited timestamp
            instance.edited_by = instance.sender  # Set the user who edited the message


@receiver(post_delete,sender=User)
def delete_user_related_data(sender,instance,**kwargs):
    instance.sent_messages.all().delete()
    instance.received_messages.all().delete()
    Notification.objects.filter(user=instance).delete()
