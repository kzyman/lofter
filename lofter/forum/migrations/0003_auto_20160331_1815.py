# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_auto_20160321_1615'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mp3',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40)),
                ('pic', models.CharField(max_length=300)),
                ('url', models.CharField(max_length=300)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='lofteruser',
            name='follower',
            field=models.ManyToManyField(related_name='user_follower', null=True, to='forum.LofterUser', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lofteruser',
            name='following',
            field=models.ManyToManyField(related_name='user_following', null=True, to='forum.LofterUser', blank=True),
            preserve_default=True,
        ),
    ]
