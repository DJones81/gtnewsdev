# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('geonewsapi', '0004_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='RetweetCount',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('date', models.DateTimeField(default=datetime.date.today)),
                ('retweetcount', models.IntegerField()),
                ('article', models.ForeignKey(to='geonewsapi.Article', related_name='retweetcount')),
            ],
        ),
    ]
