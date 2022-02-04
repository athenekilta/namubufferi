from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.views.generic import FormView

from .forms import KeycardLoginForm


class KeycardLoginFormView(FormView):
    http_method_names = ["get", "post"]
    form_class = KeycardLoginForm
    template_name = "keycards/form.html"

    def form_valid(self, form):
        user = authenticate(self.request, secret=form.cleaned_data.get("secret"))
        if user is not None:
            login(self.request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)

        form.add_error("secret", "Access denied")
        response = self.form_invalid(form)
        response.status_code = HTTPStatus.FORBIDDEN
        return response
