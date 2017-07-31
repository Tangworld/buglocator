# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locator', '0005_auto_20170731_1048'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bugidmap',
            old_name='number',
            new_name='bugidnumber',
        ),
        migrations.RenameField(
            model_name='filemap',
            old_name='number',
            new_name='filenumber',
        ),
        migrations.RenameField(
            model_name='reports',
            old_name='number',
            new_name='reportnumber',
        ),
    ]
