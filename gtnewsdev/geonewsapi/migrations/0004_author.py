# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geonewsapi', '0003_auto_20151008_1235'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('first', models.CharField(max_length=30)),
                ('last', models.CharField(max_length=30)),
                ('article', models.ForeignKey(related_name='authors', to='geonewsapi.Article')),
            ],
        ),
    ]
