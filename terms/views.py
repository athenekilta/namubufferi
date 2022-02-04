from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from .models import Terms


class TermsMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.terms.accepted:
            response = redirect("terms:update")
            response.status_code = 303
            return response
        return super().dispatch(request, *args, **kwargs)


class TermsUpdateView(LoginRequiredMixin, UpdateView):
    model = Terms
    http_method_names = ["get", "post"]
    fields = ["accepted"]
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)
    redirect_field_name = None

    def get_object(self):
        return Terms.objects.get(user=self.request.user)
