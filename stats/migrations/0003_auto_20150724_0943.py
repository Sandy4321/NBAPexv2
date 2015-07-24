# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0002_delete_referee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='birthdate',
            field=models.DateField(null=True),
        ),
    ]
