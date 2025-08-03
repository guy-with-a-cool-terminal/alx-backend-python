from django.shortcuts import render
from django.shortcuts.import redirect
from django.db.models.signals import post_delete
from .models import Message
from django.views.decorators.cache import cache_page

def get_replies(message):
    replies = message.replies.all()
    return [(reply, get_replies(reply)) for reply in replies]

@cache_page(60)
def conversation_view(request, conversation_id):
    messages = Message.objects.filter(conversation_id=conversation_id).prefetch_related('replies').select_related('sender', 'receiver')
    threaded_messages = [(message, get_replies(message)) for message in messages]
    return render(request, 'messages/conversation.html', {'threaded_messages': threaded_messages})

def inbox_view(request):
    unread_messages = Message.objects.for_user(request.user)
    return render(request, 'messages/inbox.html', {'unread_messages': unread_messages})


def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect('home')
