from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied

from .models import Conversation, Message, CustomUser
from .serializers import (
    ConversationSerializer,
    ConversationCreateSerializer,
    MessageSerializer,
)
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for conversations: list, retrieve, create.
    """
    permission_classes = [IsParticipantOfConversation]
    queryset = Conversation.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']            

    def get_serializer_class(self):
        if self.action == 'create':
            return ConversationCreateSerializer
        return ConversationSerializer

    def get_queryset(self):
        # Only show conversations where the user is a participant
        return self.queryset.filter(participants=self.request.user)

    def perform_create(self, serializer):
        # Add current user as a participant of the new conversation
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
        conversation.save()


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing messages within conversations.
    Supports listing, sending, updating, deleting messages.
    """
    permission_classes = [IsParticipantOfConversation]
    serializer_class = MessageSerializer
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter

    def get_queryset(self):
        # Only messages from conversations the user participates in
        return Message.objects.filter(
            conversation__participants=self.request.user
        ).order_by('sent_at')

    def perform_create(self, serializer):
        # Ensure user is a participant of the conversation
        conversation_id = self.request.data.get('conversation')
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            raise PermissionDenied("Conversation not found.")

        if self.request.user not in conversation.participants.all():
            # User is not a participant in this conversation
            return Response(
                {"detail": "You are not allowed to send messages to this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Save message with sender set to current user
        serializer.save(sender=self.request.user)

    def update(self, request, *args, **kwargs):
        """
        PUT / PATCH message only if user is a participant
        """
        message = self.get_object()
        if request.user not in message.conversation.participants.all():
            return Response(
                {"detail": "You are not allowed to update this message."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        DELETE message only if user is a participant
        """
        message = self.get_object()
        if request.user not in message.conversation.participants.all():
            return Response(
                {"detail": "You are not allowed to delete this message."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)
