# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0006_auto_20160424_2343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basetopic',
            name='tag',
            field=models.ManyToManyField(related_name='tag_topic', null=True, to='forum.Tag', blank=True),
            preserve_default=True,
        ),
    ]
