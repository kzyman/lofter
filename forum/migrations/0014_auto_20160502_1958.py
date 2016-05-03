# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0013_auto_20160502_1935'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='picture',
            name='description1',
        ),
        migrations.AddField(
            model_name='picture',
            name='description',
            field=models.CharField(default='a', max_length=200),
            preserve_default=False,
        ),
    ]
