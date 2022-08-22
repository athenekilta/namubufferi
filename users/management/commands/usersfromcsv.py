import csv

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

from ledger.models import Account, Product, Transaction


User = get_user_model()

class Command(BaseCommand):
    """
    Command for loading users from a csv
    
    the file should have following columns
    first_name
    last_name
    balance

    Creates accounts for all users
    """
    def add_arguments(self, parser):
        parser.add_argument("file")
        parser.add_argument("--dialect", default='unix')


    def handle(self, *args, **kwargs):
        initial_balance, created = Product.objects.get_or_create(
            defaults={'name': 'Initial balance'},
            price=0
        )

        with open(kwargs["file"]) as f:
            for row in csv.reader(f, delimiter=";"):
                print(", ".join(row))
                first_name = row[0]
                last_name = row[1]
                username =  first_name.lower() if not last_name else f"{first_name.lower()}.{last_name.lower()}"

                with transaction.atomic():
                    print(first_name, last_name, username)
                    user, created = User.objects.get_or_create(
                        defaults=dict(
                            username=username
                        ),
                        first_name=first_name,
                        last_name=last_name
                    )
                    if not created:
                        continue

                    balance = int(100*float(row[2]))
                    print(user.id)

                    account = Account.objects.get(user=user)
                    Transaction.objects.create(
                        account=account,
                        product=initial_balance,
                        price=balance,
                        quantity=1
                    )
                