# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_auto_20160422_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basetopic',
            name='tag',
            field=models.ManyToManyField(related_name='tag_topic', to='forum.Tag'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tag',
            name='tag',
            field=models.CharField(unique=True, max_length=200, blank=True),
            preserve_default=True,
        ),
    ]
