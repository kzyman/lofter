# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0006_auto_20160325_2054'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='description',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
