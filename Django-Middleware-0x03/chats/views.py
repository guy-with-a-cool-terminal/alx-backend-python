from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import filters

from .models import Conversation, Message, CustomUser
from .serializers import (
    ConversationSerializer,
    ConversationCreateSerializer,
    MessageSerializer,
)

class ConversationViewSet(viewsets.ModelViewSet):
    """ allows listing, retrieving, creating convos """
    permission_classes = [IsAuthenticated]
    queryset = Conversation.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']            

    def get_serializer_class(self):
        if self.action == 'create':
            return ConversationCreateSerializer
        return ConversationSerializer

    def get_queryset(self):
        # show conversations where the current user is a participant
        return self.queryset.filter(participants=self.request.user)

    def perform_create(self, serializer):
        # save convo and add the user to participants
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
        conversation.save()


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing messages within conversations.
    Allows listing and sending messages.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        # Show only messages in conversations the user is part of
        return Message.objects.filter(
            conversation__participants=self.request.user
        ).order_by('sent_at')

    def perform_create(self, serializer):
        # Automatically set sender to current user
        serializer.save(sender=self.request.user)

