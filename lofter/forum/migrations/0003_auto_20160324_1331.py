# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_auto_20160321_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lofteruser',
            name='follower',
            field=models.ManyToManyField(related_name='user_follower', null=True, to='forum.LofterUser', blank=True),
        ),
        migrations.AlterField(
            model_name='lofteruser',
            name='following',
            field=models.ManyToManyField(related_name='user_following', null=True, to='forum.LofterUser', blank=True),
        ),
    ]
