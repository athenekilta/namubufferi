# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-17 18:50
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('namubufferiapp', '0002_auto_20170115_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='magic_token_ttl',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 17, 19, 5, 20, 87978, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='usertag',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]