# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0009_auto_20160424_2348'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='is_deleted',
        ),
        migrations.AlterField(
            model_name='basetopic',
            name='tag',
            field=models.ManyToManyField(related_name='tag_topic', null=True, to='forum.Tag', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='to_other',
            field=models.ForeignKey(related_name='other', verbose_name='\u63d0\u5230\u7684\u4eba', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lofteruser',
            name='avatar',
            field=models.ImageField(null=True, upload_to=b'media/user/', blank=True),
            preserve_default=True,
        ),
    ]
