# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_auto_20160325_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basetopic',
            name='created_by',
            field=models.ForeignKey(related_name='author_topic', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='event',
            name='author',
            field=models.ForeignKey(verbose_name='\u53d1\u8d77\u4eba', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='event',
            name='to_other',
            field=models.ForeignKey(related_name='other', verbose_name='\u63d0\u5230\u7684\u4eba', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='owner',
            field=models.ForeignKey(related_name='forum_favorite_related', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='reply',
            name='replyer',
            field=models.ForeignKey(related_name='user_reply', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='owner',
            field=models.ForeignKey(related_name='forum_subscription_related', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
