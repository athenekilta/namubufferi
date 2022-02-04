from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import TemplateView


class Index(TemplateView):
    http_method_names = ["get"]
    template_name = "landing/index.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().get(request, *args, **kwargs)
