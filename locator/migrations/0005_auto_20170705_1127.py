# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locator', '0004_product_prouser'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='bugid',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='report',
            name='keywords',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
