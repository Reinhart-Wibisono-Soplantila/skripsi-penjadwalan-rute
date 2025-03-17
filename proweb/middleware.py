# myapp/middleware.py
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user is authenticated and not in the exempt URLs
        if not request.user.is_authenticated:
            login_url = reverse(settings.LOGIN_URL)
            if not request.path.startswith(login_url) and not request.path.startswith('/static/'):
                return redirect(login_url)  # Adjust to your login URL name
        else:
            login_url = reverse(settings.LOGIN_URL)
            if request.path == login_url:
                return redirect(settings.LOGIN_REDIRECT_URL)
        response = self.get_response(request)
        return response