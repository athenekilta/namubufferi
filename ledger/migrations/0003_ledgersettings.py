# Generated by Django 3.2.11 on 2023-02-19 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0002_account_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='LedgerSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mp_last', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]