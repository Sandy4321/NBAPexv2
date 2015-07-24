# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0005_auto_20150724_1008'),
    ]

    operations = [
        migrations.AddField(
            model_name='playeradvancedseason',
            name='league_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='playerpergameseason',
            name='league_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='playertotalseason',
            name='league_id',
            field=models.IntegerField(default=0),
        ),
    ]
