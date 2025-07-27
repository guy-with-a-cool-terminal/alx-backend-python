# chats/middleware.py

import time
from django.http import HttpResponseTooManyRequests
from collections import defaultdict

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_history = defaultdict(list)  # {ip: [timestamps]}

    def __call__(self, request):
        if request.method == 'POST' and request.path.startswith('/chat'):  # Or any specific chat URL
            ip = self.get_client_ip(request)
            current_time = time.time()

            # Remove timestamps older than 60 seconds
            self.message_history[ip] = [
                t for t in self.message_history[ip]
                if current_time - t < 60
            ]

            if len(self.message_history[ip]) >= 5:
                return HttpResponseTooManyRequests("Rate limit exceeded. Try again later.")

            self.message_history[ip].append(current_time)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
