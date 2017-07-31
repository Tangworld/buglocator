# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locator', '0007_auto_20170731_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reports',
            name='content',
            field=models.TextField(max_length=500, null=True, blank=True),
        ),
    ]
