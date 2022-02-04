import csv
import io
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.mail import mail_admins
from django.core.management.base import BaseCommand
from django.utils import timezone

User = get_user_model()


def to_currency(integer):
    return (Decimal(integer) / Decimal(100)).quantize(Decimal("0.01"))


class Command(BaseCommand):
    help = "Send user balances to admins"

    def handle(self, *args, **options):
        data = [
            (user.email, to_currency(user.account.balance))
            for user in User.objects.order_by("email")
        ]
        message = io.StringIO()
        writer = csv.writer(message)

        negative_balance = positive_balance = to_currency(0)
        message.write("# Accounts by email\n")
        for row in data:
            writer.writerow(row)
            balance = row[1]
            if balance < 0:
                negative_balance += abs(balance)
            else:
                positive_balance += balance
        overall_balance = positive_balance - negative_balance

        message.write("\n# Accounts by balance\n")
        for row in sorted(data, key=lambda row: row[1]):
            writer.writerow(row)

        message.write(
            f"\nBalance: {positive_balance} - {negative_balance} = {overall_balance}\n",
        )

        mail_admins(
            subject=f"Balance sheet {timezone.localtime()}",
            message=message.getvalue(),
        )
