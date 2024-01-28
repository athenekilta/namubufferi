from distutils.util import strtobool

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import RedirectView
from django.views import View
from ledger.raw_sql import get_debts

from jsonapi.views import (
    JSONAPICreateView,
    JSONAPIDeleteView,
    JSONAPIDetailView,
    JSONAPIListView,
)
from ledger.models import Account, Barcode, Group, Product, Transaction
from terms.views import TermsMixin

User = get_user_model()


class ListRestrictMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        if not strtobool(self.request.GET.get("list_restrict", "1")):
            if not self.request.user.is_superuser:
                raise PermissionDenied()
            return queryset
        return eval(f"queryset.filter({self.list_restrict})")


class LoginRequiredMixin(LoginRequiredMixin):
    raise_exception = True


class ObjectPermissionMixin:
    def get_object(self):
        # https://docs.djangoproject.com/en/3.2/topics/class-based-views/generic-display/#performing-extra-work
        obj = super().get_object()
        if (
            eval(self.object_permission) != self.request.user
            and not self.request.user.is_superuser
        ):
            raise PermissionDenied()
        return obj


class JSONAPICreateView(JSONAPICreateView):
    template_name = "api/form.html"


class JSONAPIDeleteView(JSONAPIDeleteView):
    template_name = "api/confirm_delete.html"


class JSONAPIDetailView(JSONAPIDetailView):
    template_name = "api/detail.html"


class JSONAPIListView(JSONAPIListView):
    template_name = "api/list.html"
    paginate_by = 10
    paginate_orphans = 5


class AccountDetailView(
    LoginRequiredMixin, TermsMixin, ObjectPermissionMixin, JSONAPIDetailView
):
    model = Account
    http_method_names = ["get"]
    object_permission = "obj.user"


class AccountListView(
    LoginRequiredMixin, TermsMixin, ListRestrictMixin, JSONAPIListView
):
    model = Account
    http_method_names = ["get"]
    list_restrict = "pk=self.request.user.account.pk"


class BarcodeCreateView(LoginRequiredMixin, TermsMixin, JSONAPICreateView):
    model = Barcode
    http_method_names = ["get", "post"]
    fields = ["id", "product"]

    def get_success_url(self):
        return reverse("api:barcode-detail", kwargs={"pk": self.object.pk})


class BarcodeListView(LoginRequiredMixin, TermsMixin, JSONAPIListView):
    model = Barcode
    http_method_names = ["get", "post"]


class BarcodeDeleteView(LoginRequiredMixin, TermsMixin, JSONAPIDeleteView):
    model = Barcode
    http_method_names = ["get", "post", "delete"]

    def get_success_url(self):
        return reverse("api:barcode-list")


class BarcodeDetailView(LoginRequiredMixin, TermsMixin, JSONAPIDetailView):
    model = Barcode
    http_method_names = ["get", "delete"]
    delete_view = BarcodeDeleteView


class GroupDetailView(LoginRequiredMixin, TermsMixin, JSONAPIDetailView):
    model = Group
    http_method_names = ["get"]


class GroupListView(LoginRequiredMixin, TermsMixin, JSONAPIListView):
    model = Group
    http_method_names = ["get"]


class ProductDetailView(LoginRequiredMixin, TermsMixin, JSONAPIDetailView):
    model = Product
    http_method_names = ["get"]


class ProductListView(LoginRequiredMixin, TermsMixin, JSONAPIListView):
    model = Product
    http_method_names = ["get"]

class DebtListView(View):
    http_method_names = ["get"]

    def get(self):
        return get_debts()

class TransactionCreateView(LoginRequiredMixin, TermsMixin, JSONAPICreateView):
    model = Transaction
    http_method_names = ["get", "post"]
    fields = ["product", "quantity"]

    def form_valid(self, form):
        form.instance.account = self.request.user.account
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("api:transaction-detail", kwargs={"pk": self.object.pk})


class TransactionDeleteView(
    LoginRequiredMixin, TermsMixin, ObjectPermissionMixin, JSONAPIDeleteView
):
    model = Transaction
    http_method_names = ["get", "post"]
    object_permission = "obj.account.user"

    def get_success_url(self):
        return reverse("api:transaction-list")


class TransactionDetailView(
    LoginRequiredMixin, TermsMixin, ObjectPermissionMixin, JSONAPIDetailView
):
    model = Transaction
    http_method_names = ["get", "delete"]
    delete_view = TransactionDeleteView
    object_permission = "obj.account.user"


@method_decorator(never_cache, name="dispatch")
class TransactionListView(
    LoginRequiredMixin, TermsMixin, ListRestrictMixin, JSONAPIListView
):
    model = Transaction
    http_method_names = ["get", "post"]
    create_view = TransactionCreateView
    list_restrict = "account=self.request.user.account"


class UserDetailView(
    LoginRequiredMixin, TermsMixin, ObjectPermissionMixin, JSONAPIDetailView
):
    model = User
    http_method_names = ["get"]
    object_permission = "obj"


class UserListView(LoginRequiredMixin, TermsMixin, ListRestrictMixin, JSONAPIListView):
    model = User
    http_method_names = ["get"]
    list_restrict = "pk=self.request.user.pk"


class UserRedirectView(LoginRequiredMixin, TermsMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        return reverse("api:user-detail", kwargs={"pk": self.request.user.pk})
