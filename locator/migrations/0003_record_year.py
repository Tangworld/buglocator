# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locator', '0002_record'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='year',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
    ]
