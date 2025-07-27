from rest_framework import permissions
from .models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to:
    - Allow access only to authenticated users
    - Restrict all operations (GET, POST, PUT, PATCH, DELETE) to participants
    of a given conversation.
    """

    def has_permission(self, request, view):
        # All requests require authentication
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission:
        Allow access only if the user is a participant of the related conversation.
        """

        # Covers GET, PUT, PATCH, DELETE on Conversations
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()

        # Covers all operations on Messages (view, update, delete)
        if isinstance(obj, Message):
            return request.user in obj.conversation.participants.all()

        # Deny access by default
        return False
