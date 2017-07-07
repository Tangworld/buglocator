# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locator', '0005_auto_20170705_1127'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='isadmin',
            field=models.CharField(max_length=32, null=True, blank=True),
        ),
    ]
