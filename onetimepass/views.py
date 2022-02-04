from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseGone, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views.generic import CreateView, FormView
from django.views.generic.base import TemplateView

from .forms import OneTimePassCheckForm, OneTimePassForm
from .models import OneTimePass
from .utils import random_pin


class OneTimePassCreateView(CreateView):
    http_method_names = ["get", "post"]
    form_class = OneTimePassForm
    template_name = "onetimepass/form.html"

    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.status_code = HTTPStatus.BAD_REQUEST
        return response

    def form_valid(self, form):
        try:
            existing = OneTimePass.objects.get(email=form.cleaned_data.get("email"))
            if existing.is_alive:
                return redirect(existing.get_check_url())
            existing.delete()
        except OneTimePass.DoesNotExist:
            pass

        password = random_pin()
        onetimepass = OneTimePass.objects.create(password=password, **form.cleaned_data)

        send_mail(
            subject="One-Time Password",
            message=render_to_string("onetimepass/email.txt", {"password": password}),
            from_email=None,
            recipient_list=[onetimepass.email],
            fail_silently=False,
            html_message=render_to_string(
                "onetimepass/email.html", {"password": password}
            ),
        )

        self.object = onetimepass
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.object.get_check_url()


class OneTimePassCheckFormView(FormView):
    http_method_names = ["get", "post"]
    form_class = OneTimePassCheckForm
    template_name = "onetimepass/check.html"
    onetimepass = None

    def dispatch(self, request, *args, **kwargs):
        onetimepass = get_object_or_404(OneTimePass, pk=kwargs.get("pk"))
        if not onetimepass.is_alive:
            return HttpResponseGone("Expired", content_type="text/plain")
        if onetimepass.is_rate_limited:
            k, v = "Retry-After", onetimepass.retry_after
            return HttpResponse(
                f"{k}: {v}",
                content_type="text/plain",
                status=HTTPStatus.TOO_MANY_REQUESTS,
                headers={k: v},
            )
        self.onetimepass = onetimepass
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = authenticate(
            self.request,
            onetimepass_id=self.kwargs.get("pk"),
            password=form.cleaned_data.get("password"),
        )
        if user is not None:
            login(self.request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)

        form.add_error("password", "Incorrect")
        response = self.form_invalid(form)
        response.status_code = HTTPStatus.FORBIDDEN
        return response


class EmailTemplateView(TemplateView):
    template_name = "onetimepass/email.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["password"] = random_pin()
        return context
