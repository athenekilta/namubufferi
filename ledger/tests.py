import random
import time
import uuid

from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()

from .models import Account, Product, Transaction


class Timer:
    def __init__(self):
        self.start_time = time.perf_counter()

    def end(self):
        end_time = time.perf_counter()
        print("Took", round(end_time - self.start_time, 3), "seconds")


class TransactionTestCase(TestCase):
    def setUp(self):
        size = 10 ** 3
        t = Timer()
        print(f"Creating {size} random products and users with accounts")
        for _ in range(size):
            Product.objects.create(name=uuid.uuid4(), price=random.randint(-1000, 1000))
            User.objects.create(username=uuid.uuid4())
        t.end()

    def test_balance(self):
        products = Product.objects.all()
        accounts = Account.objects.all()
        size = 10 ** 5
        print(f"Creating {size} random transactions")
        t = Timer()
        transactions = []
        for _ in range(size):
            product = random.choice(products)
            transactions.append(
                Transaction(
                    product=product,
                    price=product.price,
                    account=random.choice(accounts),
                    quantity=random.randint(-100, 100),
                )
            )
        Transaction.objects.bulk_create(transactions)
        t.end()

        print("Asserting accounting")
        t = Timer()
        self.assertEqual(
            sum(
                (
                    Transaction.calculate_balance(product.transaction_set.all())
                    for product in products
                )
            ),
            sum((account.balance for account in accounts)),
        )
        t.end()

        print("Settling debts")
        t = Timer()
        cent = Product.objects.create(name="cent", price=1)
        for account in accounts:
            Transaction.objects.create(
                product=cent,
                account=account,
                quantity=-account.balance,
            )
        t.end()

        print(f"Calculating the balance of all {size} transactions")
        t = Timer()
        balance = Transaction.calculate_balance(Transaction.objects.all())
        t.end()
        self.assertEqual(balance, 0)
