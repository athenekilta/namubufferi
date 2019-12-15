from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from namubufferi.settings import ADMIN_EMAILS
from django.core.mail import EmailMessage
import datetime

class Command(BaseCommand):
    help = 'Send user balances to admins'

    def get_balance_str(self):
        positive_users = [x for x in User.objects.all() if x.account.balance >= 0]
        negative_users = [x for x in User.objects.all() if x.account.balance < 0]

        positive_balance = Decimal(0)
        for u in positive_users:
            positive_balance += u.account.balance
        negative_balance = Decimal(0)
        for u in negative_users:
            negative_balance += -u.account.balance

        overall_balance = positive_balance-negative_balance

        return "Balance: {} - {} == {}e".format(positive_balance, -negative_balance, overall_balance)

    def format_user(self, user):
        return "{};{}".format(user.email, user.account.balance)

    def handle(self, *args, **options):
        accountsByEmail = User.objects.order_by('email')
        accountsByBalance = sorted(User.objects.all(), key=lambda a: a.account.balance)

        email_str = "Accounts by email\n-------------\n\n"
        
        for acc in accountsByEmail:
            email_str += self.format_user(acc) + "\n"
        

        email_str += "\n\nAccounts by balance\n-------------\n\n"
        
        for acc in accountsByBalance:
            email_str += self.format_user(acc) + "\n"

        email_str += "\n\n{}\n".format(self.get_balance_str())

        mail = EmailMessage(
                subject="Namubufferi - balance sheet {}".format(datetime.date.today().ctime()),
                body=email_str,
                to=ADMIN_EMAILS
            )

        try:
            mail.send()
            self.stdout.write("Mail sent")
        except:
            self.stderr.write("Mail not sent")