from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import activate

class AuthenticationMiddleware:
    '''
    Middleware to require authentication for all views.
    '''
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        excluded_paths = (
            '/admin/',
            '/login/',
            '/signup/',
            '/signup/activate/',
            '/password_reset/',
            '/password_reset_sent/',
            '/reset/',
            '/password_reset_complete/',
            '/terms/',
            '/privacy/',
            '/manifest.json',
            '/serviceworker.js',
            '/offline/',
            '/__reload__/',
        )
        if not request.user.is_authenticated and not request.path.startswith(excluded_paths):
            return redirect(reverse('accounts:login'))
        response = self.get_response(request)
        return response
    


class UserLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_language = None
        if request.user.is_authenticated:
            user_language = request.user.language
            activate(user_language)

        response = self.get_response(request)
        return response