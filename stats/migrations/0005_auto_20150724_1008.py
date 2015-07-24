# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0004_auto_20150724_1004'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coach',
            old_name='coach_name',
            new_name='display_first_last',
        ),
    ]
