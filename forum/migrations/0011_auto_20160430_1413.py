# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0010_auto_20160428_2342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basetopic',
            name='tag',
            field=models.ManyToManyField(related_name='tag_topic', to='forum.Tag', blank=True),
        ),
        migrations.AlterField(
            model_name='lofteruser',
            name='follower',
            field=models.ManyToManyField(related_name='user_follower', to='forum.LofterUser', blank=True),
        ),
        migrations.AlterField(
            model_name='lofteruser',
            name='following',
            field=models.ManyToManyField(related_name='user_following', to='forum.LofterUser', blank=True),
        ),
    ]
