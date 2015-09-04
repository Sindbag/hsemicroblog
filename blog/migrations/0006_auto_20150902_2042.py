# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20150901_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='like_date'),
        ),
        migrations.AlterField(
            model_name='post',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='publication date'),
        ),
    ]
