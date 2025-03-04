from distutils.util import strtobool

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin as DjangoLoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import RedirectView
from django.views import View
from ledger.raw_sql import get_debts
from ledger import models


from jsonapi.views import (
    JSONAPICreateView,
    JSONAPIDeleteView,
    JSONAPIDetailView,
    JSONAPIListView,
    JSONAPIUpdateView
)
from ledger.models import Account, Barcode, Group, Product, Transaction
from terms.views import TermsMixin

User = get_user_model()


class LoginRequiredMixin(DjangoLoginRequiredMixin):
    raise_exception = True

class ListRestrictMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        if not strtobool(self.request.GET.get("list_restrict", "1")):
            if not self.request.user.is_superuser:
                raise PermissionDenied()
            return queryset
        return queryset.filter(**self.get_list_restrict())


class LoginRequiredMixin(LoginRequiredMixin):
    raise_exception = True


class ObjectPermissionMixin:
    def get_object(self):
        # https://docs.djangoproject.com/en/3.2/topics/class-based-views/generic-display/#performing-extra-work
        obj = super().get_object()
        if (
                self.get_object_owner(obj) != self.request.user
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

class JSONAPIUpdateView(JSONAPIUpdateView):
    template_name = "api/base.html"


class JSONAPIListView(JSONAPIListView):
    template_name = "api/list.html"
    paginate_by = 10
    paginate_orphans = 5


class AccountDetailView(
    LoginRequiredMixin,   ObjectPermissionMixin, JSONAPIDetailView
):
    model = Account
    http_method_names = ["get"]
    object_permission = "obj.user"

    @staticmethod
    def get_object_owner(obj):
        return obj.user


class AccountListView(LoginRequiredMixin, ListRestrictMixin, JSONAPIListView):
    model = Account
    http_method_names = ["get"]

    def get_list_restrict(self):
        return self.request.user.account.pk



class BarcodeCreateView(LoginRequiredMixin, JSONAPICreateView):
    model = Barcode
    http_method_names = ["get", "post"]
    fields = ["id", "product"]

    def get_success_url(self):
        return reverse("api:barcode-detail", kwargs={"pk": self.object.pk})


class BarcodeListView(LoginRequiredMixin, JSONAPIListView):
    model = Barcode
    http_method_names = ["get", "post"]


class BarcodeDeleteView(LoginRequiredMixin, JSONAPIDeleteView):
    model = Barcode
    http_method_names = ["get", "post", "delete"]

    def get_success_url(self):
        return reverse("api:barcode-list")


class BarcodeDetailView(LoginRequiredMixin,   JSONAPIDetailView):
    model = Barcode
    http_method_names = ["get", "delete"]
    delete_view = BarcodeDeleteView


class GroupDetailView(LoginRequiredMixin,   JSONAPIDetailView):
    model = Group
    http_method_names = ["get"]


class GroupListView(LoginRequiredMixin,   JSONAPIListView):
    model = Group
    http_method_names = ["get"]


class ProductDetailView(LoginRequiredMixin,   JSONAPIDetailView):
    model = Product
    http_method_names = ["get"]

class DebtListView(View):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        return get_debts()

class ProductListView(LoginRequiredMixin,   JSONAPIListView):
    model = Product
    http_method_names = ["get"]


class TransactionCreateView(LoginRequiredMixin,   JSONAPICreateView):
    model = Transaction
    http_method_names = ["get", "post"]
    fields = ["product", "quantity", "state"]

    def form_valid(self, form):
        form.instance.account = self.request.user.account
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("api:transaction-detail", kwargs={"pk": self.object.pk})

class TransactionUpdateView(
    LoginRequiredMixin, ObjectPermissionMixin, JSONAPIUpdateView
):
    model = Transaction
    http_method_names = ["post"]

    fields = ["state"]

    def get_success_url(self):
        return reverse("api:transaction-detail", kwargs={"pk": self.object.pk})

    @staticmethod
    def get_object_owner(obj):
        return obj.account.user

class TransactionDeleteView(
    LoginRequiredMixin,  ObjectPermissionMixin, JSONAPIDeleteView
):
    model = Transaction
    http_method_names = ["get", "post"]

    def get_success_url(self):
        return reverse("api:transaction-list")

    @staticmethod
    def get_object_owner(obj):
        return obj.account.user


class TransactionDetailView(
    LoginRequiredMixin, ObjectPermissionMixin, JSONAPIDetailView
):
    model = Transaction
    http_method_names = ["get", "delete", "patch"]
    delete_view = TransactionDeleteView
    update_view = TransactionUpdateView

    @staticmethod
    def get_object_owner(obj):
        return obj.account.user


@method_decorator(never_cache, name="dispatch")
class TransactionListView(
    LoginRequiredMixin,   ListRestrictMixin, JSONAPIListView
):
    model = Transaction
    http_method_names = ["get", "post"]
    create_view = TransactionCreateView

    def get_list_restrict(self) -> dict:
        return dict(account=self.request.user.account)


class UserDetailView(
    LoginRequiredMixin, ObjectPermissionMixin, JSONAPIDetailView
):
    model = User
    http_method_names = ["get"]

    @staticmethod
    def get_object_owner(obj):
        return obj


class UserListView(LoginRequiredMixin, ListRestrictMixin, JSONAPIListView):
    model = User
    http_method_names = ["get"]

    def get_list_restrict(self) -> dict:
        return dict(pk=self.request.user.pk)


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        return reverse("api:user-detail", kwargs={"pk": self.request.user.pk})
