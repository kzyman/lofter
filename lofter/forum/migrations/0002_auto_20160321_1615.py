# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_time', models.DateTimeField()),
                ('involved_category', models.ForeignKey(related_name='category_subscription', to='forum.Category')),
                ('involved_topic', models.ForeignKey(related_name='forum_subscription_related', blank=True, to='forum.BaseTopic', null=True)),
                ('owner', models.ForeignKey(related_name='forum_subscription_related', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='recommend',
            name='involved_topic',
        ),
        migrations.RemoveField(
            model_name='recommend',
            name='owner',
        ),
        migrations.DeleteModel(
            name='Recommend',
        ),
        migrations.RemoveField(
            model_name='basetopic',
            name='comment_num',
        ),
        migrations.RemoveField(
            model_name='basetopic',
            name='is_recommand',
        ),
        migrations.RemoveField(
            model_name='basetopic',
            name='is_reprinted',
        ),
        migrations.RemoveField(
            model_name='basetopic',
            name='like',
        ),
        migrations.RemoveField(
            model_name='basetopic',
            name='like_num',
        ),
        migrations.RemoveField(
            model_name='lofteruser',
            name='fans_num',
        ),
        migrations.RemoveField(
            model_name='lofteruser',
            name='following_num',
        ),
        migrations.RemoveField(
            model_name='lofteruser',
            name='topic_num',
        ),
        migrations.RemoveField(
            model_name='lofteruser',
            name='updata_time',
        ),
        migrations.AddField(
            model_name='basetopic',
            name='topic_type',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='basetopic',
            name='content',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='basetopic',
            name='status',
            field=models.CharField(default=b'P', max_length=10, choices=[(b'D', b'Draft'), (b'H', b'Hidden'), (b'P', b'Published')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='basetopic',
            name='tag',
            field=models.ManyToManyField(related_name='tag_topic', null=True, to='forum.Tag', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='favorite',
            name='created_time',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='favorite',
            name='involved_topic',
            field=models.ForeignKey(related_name='forum_favorite_related', blank=True, to='forum.BaseTopic', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='favorite',
            name='owner',
            field=models.ForeignKey(related_name='forum_favorite_related', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='picture',
            name='picture',
            field=models.ImageField(upload_to=b'forum/media/'),
            preserve_default=True,
        ),
    ]
