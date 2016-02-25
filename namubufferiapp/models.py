from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from decimal import Decimal
from django.contrib import admin


class UserProfile(models.Model):
    """
    Extending the built-in model 'User' using a one-to-one relationship to
    the built-in model.
    https://docs.djangoproject.com/en/1.7/topics/auth/customizing/#extending-user

    Using Field.choices as given in https://docs.djangoproject.com/en/1.7/ref/models/fields/
    """
    user = models.OneToOneField(User)
    balance = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def make_payment(self, price):
        converted_price = Decimal(price)
        self.balance -= converted_price
        self.save()

    def make_deposit(self, money):
        converted = Decimal(money)
        self.balance += converted
        self.save()


class Category(models.Model):
    name = models.TextField(unique=True)

class Product(models.Model):
    name = models.CharField(max_length=30, unique=True)
    category = models.ForeignKey(Category, related_name='products')
    price = models.FloatField(default=0)
