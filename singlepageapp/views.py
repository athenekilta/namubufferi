from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.gzip import gzip_page
from django.views.generic import TemplateView

from terms.views import TermsMixin


@method_decorator(gzip_page, "dispatch")
class Index(LoginRequiredMixin, TermsMixin, TemplateView):
    http_method_names = ["get"]
    template_name = "singlepageapp/index.html"
    redirect_field_name = None
