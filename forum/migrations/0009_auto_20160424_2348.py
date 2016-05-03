# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0008_auto_20160424_2345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basetopic',
            name='tag',
            field=models.ManyToManyField(related_name='tag_topic', null=True, to='forum.Tag'),
            preserve_default=True,
        ),
    ]
