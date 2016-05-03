# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0015_remove_picture_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='description',
            field=models.CharField(default='a', max_length=200),
            preserve_default=False,
        ),
    ]
