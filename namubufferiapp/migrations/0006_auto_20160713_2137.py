# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-13 21:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('namubufferiapp', '0005_auto_20160713_0535'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='namubufferiapp.Transaction')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='namubufferiapp.Product')),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='namubufferiapp.Transaction')),
            ],
        ),
        migrations.RemoveField(
            model_name='sale',
            name='product',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='transaction',
        ),
        migrations.DeleteModel(
            name='Sale',
        ),
    ]