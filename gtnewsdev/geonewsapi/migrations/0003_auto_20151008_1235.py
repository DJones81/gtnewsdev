# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geonewsapi', '0002_keyword'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyword',
            name='article',
            field=models.ForeignKey(related_name='keywords', to='geonewsapi.Article'),
        ),
    ]
