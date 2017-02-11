# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-11 21:48
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
from decimal import *

def check_balances(apps, schema_editor):
    Account = apps.get_model("namubufferiapp", "Account")
    Transaction = apps.get_model("namubufferiapp", "Transaction")

    for account in Account.objects.all():
        balance_by_transaction = Decimal(0)
        for transaction in Transaction.objects.filter(customer=account).filter(canceled=False):
            balance_by_transaction += transaction.amount

        balance_diff = account.balance - balance_by_transaction

        tran = Transaction.objects.create(amount=balance_diff, customer=account)
        tran.save()

        print("For {} balance diff was {}".format(str(account), balance_diff))


class Migration(migrations.Migration):

    dependencies = [
        ('namubufferiapp', '0007_auto_20170211_2052'),
    ]

    operations = [
        migrations.RunPython(check_balances),
        migrations.RemoveField(
            model_name='account',
            name='balance',
        ),
        migrations.AlterField(
            model_name='account',
            name='magic_token_ttl',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 11, 22, 3, 4, 648361, tzinfo=utc)),
        ),
    ]