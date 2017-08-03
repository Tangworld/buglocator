# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locator', '0010_auto_20170802_0719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='description',
            field=models.TextField(max_length=700, null=True, blank=True),
        ),
    ]
