import uuid
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


def generate_magic_token():
    return str(uuid.uuid4()).upper().replace("-", "")[0:5]


class Tag(models.Model):
    """
    A tag that represents things like NFC-tag, barcode etc.
    """

    uid = models.CharField(max_length=128, blank=False, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.uid


class UserTag(Tag):
    """
    A tag representing user's identification info
    """

    user = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now_add=True)
    timestamp.editable = False


class Account(models.Model):
    # https://docs.djangoproject.com/en/1.11/topics/auth/customizing/#extending-user
    user = models.OneToOneField(User)
    magic_token = models.CharField(max_length=44, null=True, blank=True)
    magic_token_ttl = models.DateTimeField(default=timezone.now)
    tos_accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    @property
    def balance(self):
        cur_balance = Decimal(0)
        transactions = Transaction.objects.filter(customer=self).filter(canceled=False)

        for transaction in transactions:
            cur_balance += transaction.amount

        return cur_balance

    """
    Magic token allows user to login by email with unique
    link that is alive only for 15 minutes
    """

    def deactivate_magic_token(self):
        self.magic_token = None
        self.magic_token_ttl = timezone.now()
        self.save()

    def magic_token_is_alive(self):
        return timezone.now() < self.magic_token_ttl

    def update_magic_token(self):
        self.magic_token_ttl = timezone.now() + timedelta(minutes=15)
        magic_token = generate_magic_token()
        while len(Account.objects.filter(magic_token=str(magic_token))) != 0:
            magic_token = generate_magic_token()
        self.magic_token = magic_token
        self.save()
        return self.magic_token


@receiver(post_save, sender=User)
def handle_user_save(sender, instance, created, **kwargs):
    """
    If an user is created directly by User.objects, without
    this function, it wouldn't have account-instance
    """
    if created:
        acc = Account.objects.create(user=instance)
        acc.save()
        acc.update_magic_token()


class Category(models.Model):
    """
    Mainly category for products, but could also used
    for something else
    """

    name = models.CharField(max_length=30, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=128, unique=True)
    category = models.ForeignKey(Category, related_name="products")
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=1,
    )

    inventory = models.IntegerField(default=1)
    hidden = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def cancel_sale(self):
        self.inventory += 1
        self.save()

    def make_sale(self):
        self.inventory += -1
        self.save()


class ProductTag(Tag):
    """
    A tag representing product's identity (like barcode)
    """

    product = models.ForeignKey(Product)


class Transaction(models.Model):
    """
    One transaction

    Positive amount means money going into user's account,
    negative amount means money going away from user's account.

    Amount can't be derived from product as products might have
    different prices at different times.

    Canceled-flag should be noted for example when calculating
    balance from all transactions.
    """

    amount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    customer = models.ForeignKey(Account, null=True)
    product = models.ForeignKey(Product, null=True)
    canceled = models.BooleanField(default=False)
    comment = models.CharField(max_length=256, null=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        if self.customer is not None:
            return "%s, %s, %s" % (
                self.get_date_string(),
                self.customer.user.username,
                self.amount,
            )
        else:
            return "%s, %s" % (self.get_date_string(), self.amount)

    def cancel(self):
        if not self.canceled:
            self.canceled = True
            self.save()
            if self.product:
                self.product.cancel_sale()

    def get_date_string(self):
        DATE_FORMAT = "%Y-%m-%d"
        TIME_FORMAT = "%H:%M:%S"

        if self.timestamp:
            return self.timestamp.strftime("%s %s" % (DATE_FORMAT, TIME_FORMAT))
