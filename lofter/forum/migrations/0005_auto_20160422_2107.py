# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_auto_20160413_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='basetopic',
            name='Mp3',
            field=models.OneToOneField(null=True, blank=True, to='forum.Mp3'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='picture',
            name='picture',
            field=models.ImageField(upload_to=b'media/'),
            preserve_default=True,
        ),
    ]
