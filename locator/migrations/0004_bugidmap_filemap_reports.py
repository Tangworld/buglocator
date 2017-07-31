# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locator', '0003_record_year'),
    ]

    operations = [
        migrations.CreateModel(
            name='bugidmap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('index', models.CharField(max_length=20, null=True, blank=True)),
                ('bugid', models.CharField(max_length=20, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='filemap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('index', models.CharField(max_length=20, null=True, blank=True)),
                ('filepath', models.CharField(max_length=200, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='reports',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('index', models.CharField(max_length=20, null=True, blank=True)),
                ('content', models.CharField(max_length=200, null=True, blank=True)),
            ],
        ),
    ]
