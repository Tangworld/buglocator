# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locator', '0009_f2w'),
    ]

    operations = [
        migrations.CreateModel(
            name='wordmap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('wordID', models.CharField(max_length=20, null=True, blank=True)),
                ('word', models.TextField(max_length=500, null=True, blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='f2w',
            name='keywords',
            field=models.TextField(max_length=200, null=True, blank=True),
        ),
    ]
