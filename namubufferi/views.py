from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView


class RootRedirectView(LoginRequiredMixin, RedirectView):
    raise_exception = True
    permanent = False
    pattern_name = "singlepageapp:index"
