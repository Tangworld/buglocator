# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locator', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('b1', models.CharField(max_length=20, null=True, blank=True)),
                ('b2', models.CharField(max_length=20, null=True, blank=True)),
                ('b3', models.CharField(max_length=20, null=True, blank=True)),
                ('b4', models.CharField(max_length=20, null=True, blank=True)),
                ('b5', models.CharField(max_length=20, null=True, blank=True)),
                ('b6', models.CharField(max_length=20, null=True, blank=True)),
                ('b7', models.CharField(max_length=20, null=True, blank=True)),
                ('b8', models.CharField(max_length=20, null=True, blank=True)),
                ('b9', models.CharField(max_length=20, null=True, blank=True)),
                ('b10', models.CharField(max_length=20, null=True, blank=True)),
                ('b11', models.CharField(max_length=20, null=True, blank=True)),
                ('b12', models.CharField(max_length=20, null=True, blank=True)),
                ('f1', models.CharField(max_length=20, null=True, blank=True)),
                ('f2', models.CharField(max_length=20, null=True, blank=True)),
                ('f3', models.CharField(max_length=20, null=True, blank=True)),
                ('f4', models.CharField(max_length=20, null=True, blank=True)),
                ('f5', models.CharField(max_length=20, null=True, blank=True)),
                ('f6', models.CharField(max_length=20, null=True, blank=True)),
                ('f7', models.CharField(max_length=20, null=True, blank=True)),
                ('f8', models.CharField(max_length=20, null=True, blank=True)),
                ('f9', models.CharField(max_length=20, null=True, blank=True)),
                ('f10', models.CharField(max_length=20, null=True, blank=True)),
                ('f11', models.CharField(max_length=20, null=True, blank=True)),
                ('f12', models.CharField(max_length=20, null=True, blank=True)),
                ('userid', models.CharField(max_length=20, null=True, blank=True)),
            ],
        ),
    ]
