# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20150901_2322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 1, 20, 26, 55, 897103, tzinfo=utc), verbose_name='like_date'),
        ),
        migrations.AlterField(
            model_name='post',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 1, 20, 26, 55, 896030, tzinfo=utc), verbose_name='publication date'),
        ),
    ]
