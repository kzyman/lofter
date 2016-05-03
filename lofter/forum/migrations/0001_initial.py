# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseTopic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=20)),
                ('content', models.TextField(null=True)),
                ('music', models.URLField(null=True, blank=True)),
                ('music_picture', models.CharField(max_length=300, blank=True)),
                ('vedio', models.URLField(null=True, blank=True)),
                ('recommand_num', models.IntegerField(default=0, verbose_name='\u63a8\u8350\u6570\u76ee', blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(null=True, blank=True)),
                ('is_recommand', models.BooleanField(default=False, verbose_name='\u662f\u5426\u63a8\u8350')),
                ('is_reprinted', models.BooleanField(default=False, verbose_name='\u662f\u5426\u8f6c\u8f7d')),
                ('like_num', models.IntegerField(default=0, verbose_name='\u559c\u6b22\u6570\u76ee')),
                ('like', models.BooleanField(default=False, verbose_name='\u662f\u5426\u6807\u8bb0\u559c\u6b22')),
                ('comment_num', models.IntegerField(default=0)),
                ('status', models.CharField(max_length=10, choices=[(b'D', b'Draft'), (b'H', b'Hidden'), (b'P', b'Published')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=20)),
                ('description', models.CharField(max_length=100)),
                ('involved', models.IntegerField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('recommend', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('status', models.IntegerField()),
                ('is_read', models.BooleanField(default=False, verbose_name='\u5df2\u8bfb')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='\u5df2\u5220\u9664')),
                ('submint_time', models.DateTimeField(auto_now_add=True, verbose_name='\u65f6\u95f4')),
                ('author', models.ForeignKey(verbose_name='\u53d1\u8d77\u4eba', to=settings.AUTH_USER_MODEL)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('to_other', models.ForeignKey(related_name='other', verbose_name='\u63d0\u5230\u7684\u4eba', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('involved_topic', models.ForeignKey(related_name='topic_favor', blank=True, to='forum.BaseTopic', null=True)),
                ('owner', models.ForeignKey(related_name='user_favor', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LofterUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_name', models.CharField(max_length=10)),
                ('avatar', models.ImageField(null=True, upload_to=b'', blank=True)),
                ('description', models.CharField(max_length=500, blank=True)),
                ('topic_num', models.IntegerField(default=0)),
                ('fans_num', models.IntegerField(default=0)),
                ('following_num', models.IntegerField(default=0)),
                ('updata_time', models.TimeField(auto_now_add=True, null=True)),
                ('follower', models.ManyToManyField(related_name='user_follower', to='forum.LofterUser')),
                ('following', models.ManyToManyField(related_name='user_following', to='forum.LofterUser')),
                ('users', models.OneToOneField(related_name='common_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('picture', models.ImageField(upload_to=b'')),
                ('topic', models.ForeignKey(related_name='topic_picture', to='forum.BaseTopic')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Recommend',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_time', models.DateTimeField()),
                ('involved_topic', models.ForeignKey(related_name='topic_recommend', blank=True, to='forum.BaseTopic', null=True)),
                ('owner', models.ForeignKey(related_name='user_recommend', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('submit_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(null=True, editable=False, blank=True)),
                ('replyer', models.ForeignKey(related_name='user_reply', to=settings.AUTH_USER_MODEL)),
                ('topic', models.ForeignKey(related_name='topic_reply', verbose_name='\u6240\u5c5e\u4e3b\u9898', to='forum.BaseTopic')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.CharField(max_length=20, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='basetopic',
            name='category',
            field=models.ForeignKey(related_name='category_topic', blank=True, to='forum.Category', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='basetopic',
            name='created_by',
            field=models.ForeignKey(related_name='author_topic', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='basetopic',
            name='tag',
            field=models.ManyToManyField(related_name='tag_topic', null=True, to='forum.Tag'),
            preserve_default=True,
        ),
    ]
