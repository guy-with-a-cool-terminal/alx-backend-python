from rest_framework import permissions
from .models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation
    to access its messages.
    """

    def has_permission(self, request, view):
        # Ensure user is authenticated globally (already set in settings)
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # obj could be Conversation or Message instance

        # If object is a Conversation, check if user is a participant
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()

        # If object is a Message, check if user is participant of the message's conversation
        if isinstance(obj, Message):
            return request.user in obj.conversation.participants.all()

        return False
