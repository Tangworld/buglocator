# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locator', '0004_bugidmap_filemap_reports'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bugidmap',
            old_name='index',
            new_name='number',
        ),
        migrations.RenameField(
            model_name='filemap',
            old_name='index',
            new_name='number',
        ),
        migrations.RenameField(
            model_name='reports',
            old_name='index',
            new_name='number',
        ),
    ]
