# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geonewsapi', '0009_auto_20151019_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='retweetcount',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
