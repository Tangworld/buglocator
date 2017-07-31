# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locator', '0006_auto_20170731_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reports',
            name='content',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
    ]
