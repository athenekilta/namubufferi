# Generated by Django 4.2.1 on 2023-06-09 08:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customuser_terms_accepted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='terms_accepted',
        ),
    ]
