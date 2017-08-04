# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locator', '0010_auto_20170802_0719'),
    ]

    operations = [
        migrations.AddField(
            model_name='filemap',
            name='path_l2ss',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
