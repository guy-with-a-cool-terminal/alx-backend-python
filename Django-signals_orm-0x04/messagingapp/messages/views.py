from django.shortcuts import render
from django.shortcuts.import redirect
from django.db.models.signals import post_delete
from .models import Message
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required

@login_required
def send_message(request):
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver_id')
        content = request.POST.get('content')
        Message.objects.create(sender=request.user, receiver_id=receiver_id, content=content)  # Ensure sender=request.user
        return redirect('inbox')  # Redirect to inbox or another page after sending

@login_required
def inbox_view(request):
    messages = Message.objects.filter(receiver=request.user)  # Fetch messages for the logged-in user
    return render(request, 'messages/inbox.html', {'messages': messages})

def get_replies(message):
    replies = message.replies.all()
    return [(reply, get_replies(reply)) for reply in replies]

@cache_page(60)
def conversation_view(request, conversation_id):
    messages = Message.objects.filter(conversation_id=conversation_id).prefetch_related('replies').select_related('sender', 'receiver')
    threaded_messages = [(message, get_replies(message)) for message in messages]
    return render(request, 'messages/conversation.html', {'threaded_messages': threaded_messages})

def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect('home')
