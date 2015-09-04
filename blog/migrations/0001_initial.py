# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(help_text="What's new?", max_length=280)),
                ('pub_date', models.DateTimeField(verbose_name='publication date', default=django.utils.timezone.now)),
                ('likes', models.PositiveIntegerField()),
                ('answerfor', models.OneToOneField(blank=True, to='blog.Post', null=True)),
            ],
            options={
                'get_latest_by': 'pub_date',
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('website', models.URLField(blank=True)),
                ('picture', models.ImageField(blank=True, default=None, upload_to='static/avatars')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('likes', models.PositiveIntegerField()),
                ('follows', models.ManyToManyField(blank=True, related_name='followers', to='blog.UserProfile')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(to='blog.UserProfile'),
        ),
        migrations.AddField(
            model_name='post',
            name='likes_by',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
