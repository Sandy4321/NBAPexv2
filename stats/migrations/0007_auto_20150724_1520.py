# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0006_auto_20150724_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playeradvancedseason',
            name='w_pct',
            field=models.DecimalField(null=True, decimal_places=3, max_digits=4),
        ),
        migrations.AlterField(
            model_name='playerpergameseason',
            name='w_pct',
            field=models.DecimalField(null=True, decimal_places=3, max_digits=4),
        ),
        migrations.AlterField(
            model_name='playertotalseason',
            name='w_pct',
            field=models.DecimalField(null=True, decimal_places=3, max_digits=4),
        ),
    ]
