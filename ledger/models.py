from django.conf import settings
from django.db import models
from django.db.models import F, Sum

from uuidmodels.models import UUIDModel


class Account(UUIDModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.user}"

    @property
    def balance(self):
        return Transaction.calculate_balance(queryset=self.transaction_set.all().filter(state=TransactionState.COMMITTED))


class Product(UUIDModel):
    name = models.CharField(max_length=128, unique=True)
    price = models.IntegerField()
    hidden = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"

    @property
    def inventory(self):
        return self.transaction_set.aggregate(Sum("quantity"))["quantity__sum"] or 0

class TransactionState(models.IntegerChoices):
    PENDING = 0, 'pending'
    COMMITTED = 1, 'committed'

class Transaction(UUIDModel):
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price = models.IntegerField(blank=True)
    quantity = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    state = models.IntegerField(choices=TransactionState.choices, default=TransactionState.PENDING)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.timestamp}"

    def save(self, *args, **kwargs):
        if self.price is None:
            self.price = self.product.price
        super().save(*args, **kwargs)

    @staticmethod
    def calculate_balance(queryset):
        if not queryset.exists():
            return 0
        return queryset.annotate(total=F("quantity") * F("price")).aggregate(
            Sum("total")
        )["total__sum"]

    @property
    def total(self):
        return self.price * self.quantity

    @property
    def balance(self):
        return Transaction.calculate_balance(
            queryset=self.account.transaction_set.filter(timestamp__lte=self.timestamp, state=TransactionState.COMMITTED)
        )


class Group(UUIDModel):
    name = models.CharField(max_length=128, unique=True)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return f"{self.name}"


class Barcode(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}"
