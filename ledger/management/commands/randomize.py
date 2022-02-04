import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from ledger.models import Account, Product, Transaction

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        for _ in range(10 ** 2):
            randomhex = random.randbytes(8).hex()
            email = f"{randomhex}@domain.invalid"
            User.objects.create(username=email, email=email)

        products = Product.objects.all()
        transactions = []
        for account in Account.objects.all():
            for _ in range(10 ** 2):
                product = random.choice(products)
                transactions.append(
                    Transaction(
                        account=account,
                        product=product,
                        price=product.price,
                        quantity=-1,
                    )
                )
        Transaction.objects.bulk_create(transactions)
