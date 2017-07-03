# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locator', '0002_auto_20170703_0235'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('summary', models.CharField(max_length=50, null=True, blank=True)),
                ('description', models.CharField(max_length=200, null=True, blank=True)),
                ('reporter', models.CharField(max_length=32, null=True, blank=True)),
                ('assignee', models.CharField(max_length=32, null=True, blank=True)),
                ('productid', models.CharField(max_length=32, null=True, blank=True)),
                ('status', models.CharField(max_length=32, null=True, blank=True)),
                ('opendate', models.CharField(max_length=32, null=True, blank=True)),
                ('fixdate', models.CharField(max_length=32, null=True, blank=True)),
                ('method', models.CharField(max_length=32, null=True, blank=True)),
                ('fileloc', models.CharField(max_length=100, null=True, blank=True)),
                ('component', models.CharField(max_length=32, null=True, blank=True)),
                ('version', models.CharField(max_length=32, null=True, blank=True)),
                ('platform', models.CharField(max_length=32, null=True, blank=True)),
                ('os', models.CharField(max_length=32, null=True, blank=True)),
                ('priority', models.CharField(max_length=32, null=True, blank=True)),
                ('severity', models.CharField(max_length=32, null=True, blank=True)),
            ],
        ),
    ]
