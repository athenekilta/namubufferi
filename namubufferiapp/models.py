from base64 import b64encode
from datetime import timedelta
from decimal import Decimal
from hashlib import sha256
from os import urandom

from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.utils import timezone


# For old migrations
def generate_magic_key():
    system_check_removed_details = {
        'msg': (
            'generate_magic_key has been removed except for support in '
            'historical migrations.'
        ),
        'hint': 'Use generate_magic_token instead.',
    }


def generate_magic_token():
    magic = b64encode(sha256(urandom(32)).digest(), '-_'.encode('ascii'))
    print(magic)
    return magic


class Tag(models.Model):
    """
    A tag that represents things like NFC-tag, barcode etc.
    """
    uid = models.CharField(max_length=128, blank=False, unique=True)

    def __str__(self):
        return self.uid

    class Meta:
        abstract = True

class UserTag(Tag):
    """
    A tag representing user's identification info
    """
    user = models.ForeignKey(User)



class Account(models.Model):
    """
    Extending the built-in model 'User' using a one-to-one relationship to
    the built-in model.
    https://docs.djangoproject.com/en/1.7/topics/auth/customizing/#extending-user
    """
    user = models.OneToOneField(User)
    magic_token = models.CharField(max_length=44, unique=True, default=generate_magic_token)
    magic_token_ttl = models.DateTimeField(default=(timezone.now() + timedelta(minutes=15)))  # TODO: Static

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
    def update_magic_token(self):
        self.magic_token_ttl = timezone.now() + timedelta(minutes=15)
        self.magic_token = generate_magic_token()
        self.save()
        return self.magic_token

    def deactivate_magic_token(self):
        self.magic_token = generate_magic_token()
        self.magic_token_ttl = timezone.now()
        self.save()

    def magic_token_is_alive(self):
        return timezone.now() < self.magic_token_ttl

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def handle_user_save(sender, instance, created, **kwargs):
    """
    If an user is created directly by User.objects, without
    this function, it wouldn't have account-instance
    """
    if created:
        acc = Account.objects.create(user=instance)
        acc.save()


class Category(models.Model):
    """
    Mainly category for products, but could also used
    for something else
    """
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Product(models.Model):
    name = models.CharField(max_length=128, unique=True)
    category = models.ForeignKey(Category, related_name='products')
    price = models.DecimalField(max_digits=5,
                                decimal_places=2,
                                default=1,
                               )

    inventory = models.IntegerField(default=1)
    hidden = models.BooleanField(default=False)

    def make_sale(self):
        self.inventory += -1
        self.save()

    def cancel_sale(self):
        self.inventory += 1
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

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
    amount = models.DecimalField(max_digits=5,
                                 decimal_places=2,
                                 default=0,
                                 )

    timestamp = models.DateTimeField(auto_now_add=True)
    timestamp.editable = False
    customer = models.ForeignKey(Account, null=True)
    product = models.ForeignKey(Product, null=True)
    canceled = models.BooleanField(default=False)

    def get_date_string(self):
        DATE_FORMAT = "%Y-%m-%d"
        TIME_FORMAT = "%H:%M:%S"

        if self.timestamp:
            return self.timestamp.strftime("%s %s" %
                                           (DATE_FORMAT, TIME_FORMAT))

    def cancel(self):
        if not self.canceled:
            self.canceled = True
            self.save()
            if self.product:
                self.product.cancel_sale()

    def __str__(self):
        if self.customer is not None:
            return "%s, %s, %s" % (self.get_date_string(), self.customer.user.username, self.amount)
        else:
            return "%s, %s" % (self.get_date_string(), self.amount)

    class Meta:
        ordering = ["-timestamp"]
