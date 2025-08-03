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
