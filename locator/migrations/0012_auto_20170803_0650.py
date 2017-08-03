# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locator', '0011_auto_20170803_0625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='summary',
            field=models.TextField(max_length=200, null=True, blank=True),
        ),
    ]
