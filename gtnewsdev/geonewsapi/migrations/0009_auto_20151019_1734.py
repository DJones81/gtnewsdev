# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geonewsapi', '0008_auto_20151015_1636'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.CharField(max_length=28, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='article',
            name='abstract',
            field=models.CharField(max_length=500, blank=True),
        ),
    ]
