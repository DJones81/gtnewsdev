# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('geonewsapi', '0012_auto_20151105_1413'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacebookCount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('date', models.DateTimeField(default=datetime.date.today)),
                ('likecount', models.IntegerField()),
                ('commentcount', models.IntegerField()),
                ('sharecount', models.IntegerField()),
                ('clickcount', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='sharecount',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='facebookcount',
            name='article',
            field=models.ForeignKey(related_name='facebookcounts', to='geonewsapi.Article'),
        ),
    ]
