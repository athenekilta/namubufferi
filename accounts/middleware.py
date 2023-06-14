from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse

class AuthenticationMiddleware:
    '''
    Middleware to require authentication for all views.
    '''
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        excluded_paths = (
            reverse('accounts:login'),
            reverse('accounts:password_reset'),
            reverse('accounts:signup'),
            reverse('admin:index')
        )
        if not request.user.is_authenticated and not request.path.startswith(excluded_paths):
            return redirect(reverse('accounts:login'))
        response = self.get_response(request)
        return response