# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locator', '0008_auto_20170731_1111'),
    ]

    operations = [
        migrations.CreateModel(
            name='f2w',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fileID', models.CharField(max_length=20, null=True, blank=True)),
                ('keywords', models.TextField(max_length=1000, null=True, blank=True)),
            ],
        ),
    ]
