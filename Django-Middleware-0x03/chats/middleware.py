from datetime import datetime
from django.http import HttpResponseForbidden,HttpResponse
from collections import defaultdict

class RequestLoggingMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
    
    def __call__(self,request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}\n"
        
        with open("requests.log", "a")as log_file:
            log_file.write(log_entry)
        return self.get_response(request)

class RestrictAccessByTimeMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
    
    def __call__(self,request):
        now = datetime.now().time()
        start = datetime.strptime("18:00", "%H:%M").time() 
        end = datetime.strptime("21:00", "%H:%M").time()
        
        if not (start <= now <= end):
            return HttpResponseForbidden("Chat access is only allowed between 6PM and 9PM.")
        return self.get_response(request)

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
                return HttpResponse("Rate limit exceeded. Try again later.")

            self.message_history[ip].append(current_time)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Assuming your User model has a 'role' attribute
        user = request.user

        if not user.is_authenticated:
            return HttpResponseForbidden("You must be logged in.")

        allowed_roles = ['admin', 'moderator']

        # If user.role doesn't exist or user.role not in allowed_roles, block
        if not hasattr(user, 'role') or user.role not in allowed_roles:
            return HttpResponseForbidden("You do not have permission to access this resource.")

        return self.get_response(request)