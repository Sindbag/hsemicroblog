# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_remove_userprofile_likes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('pub_date', models.DateTimeField(default=datetime.datetime(2015, 9, 1, 20, 22, 36, 336971, tzinfo=utc), verbose_name='like_date')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='likes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='post',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 1, 20, 22, 36, 334969, tzinfo=utc), verbose_name='publication date'),
        ),
        migrations.AddField(
            model_name='like',
            name='author',
            field=models.ForeignKey(to='blog.UserProfile'),
        ),
        migrations.AddField(
            model_name='like',
            name='post',
            field=models.ForeignKey(to='blog.Post'),
        ),
    ]
