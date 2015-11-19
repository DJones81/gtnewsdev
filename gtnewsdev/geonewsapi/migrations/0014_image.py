# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geonewsapi', '0013_auto_20151110_0059'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('url', models.URLField()),
                ('article', models.ForeignKey(to='geonewsapi.Article', related_name='images')),
            ],
        ),
    ]
