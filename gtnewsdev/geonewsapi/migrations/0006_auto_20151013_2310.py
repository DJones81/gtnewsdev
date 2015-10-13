# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geonewsapi', '0005_retweetcount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='title',
            new_name='headline',
        ),
        migrations.AddField(
            model_name='article',
            name='abstract',
            field=models.CharField(max_length=2000, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='retweetcount',
            name='article',
            field=models.ForeignKey(to='geonewsapi.Article', related_name='retweetcounts'),
        ),
    ]
