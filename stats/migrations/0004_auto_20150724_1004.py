# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0003_auto_20150724_0943'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coach',
            options={'verbose_name_plural': 'coaches'},
        ),
        migrations.AlterField(
            model_name='player',
            name='player_id',
            field=models.IntegerField(unique=True),
        ),
    ]
