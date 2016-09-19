# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-08-18 22:58
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import namubufferiapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('namubufferiapp', '0017_auto_20160818_2212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='magic_hash',
            field=models.CharField(default=namubufferiapp.models.generate_magic_key, max_length=7, unique=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='magic_link_ttl',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 18, 23, 13, 56, 726220, tzinfo=utc)),
        ),
    ]