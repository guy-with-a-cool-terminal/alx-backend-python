from django.shortcuts import render
from django.shortcuts.import redirect
from django.db.models.signals import post_delete
from .models import Message
from django.views.decorators.cache import cache_page
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message

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

def inbox_view(request):
    unread_messages = Message.objects.for_user(request.user)
    return render(request, 'messages/inbox.html', {'unread_messages': unread_messages})


def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect('home')
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message

@login_required
def send_message(request):
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver_id')
        content = request.POST.get('content')
        Message.objects.create(sender=request.user, receiver_id=receiver_id, content=content)
        return redirect('inbox')

@login_required
def inbox_view(request):
    # Use the custom manager to get unread messages
    unread_messages = Message.unread.unread_for_user(request.user).only('id', 'content', 'timestamp')  # Optimize with .only()
    return render(request, 'messages/inbox.html', {'unread_messages': unread_messages})

