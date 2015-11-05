# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geonewsapi', '0011_auto_20151020_1455'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='article',
        ),
        migrations.AddField(
            model_name='article',
            name='byline',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='sourceid',
            field=models.CharField(unique=True, default='', max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='article',
            name='url',
            field=models.URLField(unique=True, max_length=300),
        ),
        migrations.DeleteModel(
            name='Author',
        ),
    ]
