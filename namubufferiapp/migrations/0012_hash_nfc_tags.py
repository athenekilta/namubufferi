# -*- coding: utf-8 -*-
from django.db import migrations
from django.contrib.auth.hashers import make_password

def hash_keys(apps, schema_editor):
    UserTag = apps.get_model('namubufferiapp', 'UserTag')
    for tag in UserTag.objects.all():
        oldTagUid = tag.uid
        newTagUid = make_password(oldTagUid)

        tag.uid = newTagUid
        tag.save()

class Migration(migrations.Migration):

    dependencies = [
        ('namubufferiapp', '0011_auto_20180318_1625'),
    ]

    operations = [
        migrations.RunPython(hash_keys)
    ]
